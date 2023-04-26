import typing as t
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from .config import settings


Base = declarative_base()

user = settings.db_username
password = settings.db_password
host = settings.db_host
port = settings.db_port
db_name = settings.db_name


SYNC_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> t.AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
sync_session = sessionmaker(
    sync_engine, class_=Session, expire_on_commit=False)


def get_sync_session() -> t.Iterator[Session]:
    with sync_session() as session:
        yield session

