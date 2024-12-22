from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


def update_user(telegram_id: int, **kwargs) -> None:
    with sync_session() as session:
        with session.begin():
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)