from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Md5Task
from .exceptions import TaskNotFound


async def retrieve_md5_task(session: AsyncSession, task_id: int) -> Md5Task:
    query = select(Md5Task).where(Md5Task.task_id == task_id)
    result = await session.execute(query)
    result = result.scalar()

    if not result:
        raise TaskNotFound(task_id)
    return result


def sync_retrieve_md5_task(session: Session, task_id: int) -> Md5Task:
    query = select(Md5Task).where(Md5Task.task_id == task_id)
    result = session.execute(query)
    result = result.scalar()

    if not result:
        raise TaskNotFound(task_id)
    return result

