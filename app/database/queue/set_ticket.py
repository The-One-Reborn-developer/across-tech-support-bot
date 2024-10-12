from app.database.models.ticket import Ticket
from app.database.models.sync_session import sync_session


def set_ticket(telegram_id: int, ticket_id: int, chat_id: int) -> None:
    with sync_session() as session:
        with session.begin():
            ticket = Ticket(telegram_id=telegram_id, ticket_id=ticket_id, chat_id=chat_id)

            session.add(ticket)