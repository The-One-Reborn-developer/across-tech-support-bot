from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


def get_user(telegram_id: int) -> User | None:
    with sync_session() as session:
        with session.begin():
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                return [
                    user.name,
                    user.position,
                    user.region,
                    user.phone,
                    user.medical_organization
                ]
            
            return None