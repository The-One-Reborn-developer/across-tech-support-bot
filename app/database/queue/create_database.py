from app.database.models.base import Base
from app.database.models.engine import engine


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)