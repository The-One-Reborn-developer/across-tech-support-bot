from sqlalchemy import select

from app.database.models.user import User
from app.database.models.async_session import async_session


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            data = []

            if user:
                data.append(user.name)
                data.append(user.position)
                data.append(user.region)
                data.append(user.phone)
                data.append(user.medical_organization)
            else:
                return None

            return data