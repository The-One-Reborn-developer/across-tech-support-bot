from sqlalchemy import select

from app.database.models.ticket import Ticket
from app.database.models.sync_session import sync_session


def get_all_user_tickets(telegram_id: int) -> list | None:
    with sync_session() as session:
        with session.begin():
            tickets = session.scalars(select(Ticket).where(Ticket.telegram_id == telegram_id))

            return [ticket.ticket_id for ticket in tickets.all()]