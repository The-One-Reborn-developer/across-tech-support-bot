from sqlalchemy import select

from app.database.models.user import User
from app.database.models.sync_session import sync_session


def set_user(telegram_id: int) -> None:
    with sync_session() as session:
        with session.begin():
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)