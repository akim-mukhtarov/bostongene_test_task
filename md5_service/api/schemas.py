from pydantic import BaseModel
from md5_task_data.constants import TaskStatus


class Md5TaskId(BaseModel):
    task_id: int


class Md5Task(BaseModel):
    status: TaskStatus
    result: str | None

    class Config:
        orm_mode = True

