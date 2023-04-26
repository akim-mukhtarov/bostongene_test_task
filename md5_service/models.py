from sqlalchemy import Column, Integer, String, LargeBinary, Enum
from .database import Base
from .constants import TaskStatus


class Md5Task(Base):
    """Represents the process of computing MD5 hash."""
    __tablename__ = 'md5_tasks'

    task_id = Column(Integer(), primary_key=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    result = Column(String())

