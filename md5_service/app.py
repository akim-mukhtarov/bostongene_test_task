import os
import uuid
from fastapi import FastAPI, UploadFile, Depends
from .tasks import compute_md5_hash
from .database import get_session
from .crud import retrieve_md5_task
from . import models
from . import schemas


app = FastAPI()


@app.post("/hashes/")
async def compute_hash(file: UploadFile, session = Depends(get_session)):
    """Compute MD5 hash asynchronously."""
    # Save file in shared directory. Consider moving to utils save_file() -> path
    filename = str(uuid.uuid4())             # unique filename
    path = os.path.join('/tmp', filename)    # or whatever shared_dir is used
    with open(path, 'wb') as data:
        data.write(await file.read())

    task = models.Md5Task()
    session.add(task)
    await session.commit()
    # consider deleting Md5Task in case sending fails
    compute_md5_hash.delay(filename, task.task_id)
    return schemas.Md5TaskId(task_id=task.task_id)


@app.get("/hashes/{task_id}")
async def retrieve_hash(task_id: int, session = Depends(get_session)):
    """Retrieve MD5 hash."""
    task = await retrieve_md5_task(session, task_id)
    return schemas.Md5Task.from_orm(task)

