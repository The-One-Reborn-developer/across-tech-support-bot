from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.models.async_engine import async_engine


async_session = async_sessionmaker(async_engine, expire_on_commit=False)