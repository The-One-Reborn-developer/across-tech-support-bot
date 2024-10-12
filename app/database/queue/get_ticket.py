from sqlalchemy import select

from app.database.models.ticket import Ticket
from app.database.models.sync_session import sync_session


def get_ticket(ticket_id: int) -> Ticket | None:
    with sync_session() as session:
        with session.begin():
            ticket = session.scalar(select(Ticket).where(Ticket.ticket_id == ticket_id))

            if ticket:
                return [
                    ticket.ticket_id,
                    ticket.telegram_id,
                    ticket.chat_id
                ]
            
            return None