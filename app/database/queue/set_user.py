from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


async def set_user(telegram_id: int) -> None:
    async with sync_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                await session.commit()