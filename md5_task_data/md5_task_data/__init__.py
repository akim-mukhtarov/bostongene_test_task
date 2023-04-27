import asyncio
from .database import Base, engine


async def init_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


loop = asyncio.get_event_loop()
asyncio.ensure_future(init_connection(), loop=loop)
