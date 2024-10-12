from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


async def update_user(telegram_id: int, **kwargs) -> None:
    async with sync_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)

                await session.commit()