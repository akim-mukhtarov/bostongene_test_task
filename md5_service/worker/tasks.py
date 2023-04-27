import os
import time
import fcntl
import hashlib
import logging
from celery import Celery, chain
from md5_task_data.database import get_sync_session
from md5_task_data.crud import sync_retrieve_md5_task
from md5_task_data.constants import TaskStatus
from .config import settings


celery = Celery('MD5 Hashes',
                broker=settings.celery_broker_url,
                result_backend=settings.celery_result_backend_url)


logfile = settings.logfile
lockfile = os.path.join(os.path.dirname(logfile), '.lock')

file_handler = logging.handlers.WatchedFileHandler(logfile, mode='a')
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('MD5 Hashes')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# lockfile must be in a shared dir
@celery.task(bind=True, max_retries=3)
def log(self, message):
    logger = logging.getLogger('MD5 Hashes')

    if not os.path.exists(lockfile):
        os.system("touch %s" %(lockfile))    # consider `create` instead

    f = open(lockfile, "w")    # consider contextmanager

    try:
        fcntl.lockf(f.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
    except OSError as e:
        print("can't get lock for mysql %s, please check script is already running")
        self.retry(exc=e, countdown=5)
    else:
        logger.debug("get file lock on %s success" %(lockfile))
        logger.info(message)
    finally:
        f.close()


@celery.task
def save_error(task_id, error):
    session = next(get_sync_session())
    celery_task_id = self.request.id
    task = sync_retrieve_md5_task(session, task_id)
    task.result = str(error)
    task.status = TaskStatus.ERROR
    session.add(task)
    session.commit()


@celery.task
def save_result(task_id, result):
    session = next(get_sync_session())
    task = sync_retrieve_md5_task(session, task_id)
    task.result = result
    task.status = TaskStatus.SUCCESS
    session.add(task)
    session.commit()


@celery.task
def report_error(task_id, error):
    time.sleep(5)    # Dirty solution, consider another approach
    msg = f"An error has occured while computing MD5: {error}"
    chain(log.si(msg), save_error.si(task_id, error)).apply_async()


@celery.task
def report_success(task_id, result):
    time.sleep(5)    # Dirty solution, consider another approach
    msg = f"Computed MD5: {result}"
    chain(log.si(msg), save_result.si(task_id, result)).apply_async()


@celery.task
def compute_md5_hash(filename, task_id):
    try:
        filename = os.path.join('/tmp', filename)
        with open(filename, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        md5 = file_hash.hexdigest()

    except Exception as e:
        report_error.delay(task_id, e)
    else:
        report_success.delay(task_id, md5)

