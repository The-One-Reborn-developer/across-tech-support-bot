from sqlalchemy import select

from app.database.models.ticket import Ticket
from app.database.models.sync_session import sync_session


def delete_ticket(ticket_id: int) -> None:
    with sync_session() as session:
        with session.begin():
            ticket = session.scalar(select(Ticket).where(Ticket.ticket_id == ticket_id))

            if ticket:
                session.delete(ticket)