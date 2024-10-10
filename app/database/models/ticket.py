from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=True)
    chat_id = mapped_column(BigInteger, nullable=True)