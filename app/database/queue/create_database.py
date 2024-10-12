from app.database.models.base import Base
from app.database.models.sync_engine import sync_engine


async def create_database() -> None:
    async with sync_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)