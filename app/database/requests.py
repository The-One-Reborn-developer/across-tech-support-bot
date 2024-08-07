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


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            data = []

            data.append(user.name)
            data.append(user.position)
            data.append(user.region)
            data.append(user.phone)
            data.append(user.medical_organization)

            return data
        

async def update_user(telegram_id: int, **kwargs) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)

                await session.commit()