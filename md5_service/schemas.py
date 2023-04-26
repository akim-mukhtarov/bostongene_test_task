from pydantic import BaseModel
from .constants import TaskStatus


class Md5TaskId(BaseModel):
    task_id: int


class Md5Task(BaseModel):
    status: TaskStatus
    result: str

    class Config:
        orm_mode = True
