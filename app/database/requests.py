from app.database.models import async_session
from app.database.models import User

from sqlalchemy import select, update


async def set_user(telegram_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                await session.commit()


async def get_user(telegram_id: int) -> User:
    async with async_session() as session:
        async with session.begin():
            return await session.scalars(select(User))