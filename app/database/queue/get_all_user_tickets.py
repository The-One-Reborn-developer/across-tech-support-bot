from sqlalchemy import select

from app.database.models.ticket import Ticket
from app.database.models.async_session import async_session


async def get_all_user_tickets(telegram_id: int) -> list | None:
    async with async_session() as session:
        async with session.begin():
            tickets = await session.scalars(select(Ticket).where(Ticket.telegram_id == telegram_id))

            tickets_all = tickets.all()

            ticket_ids = []

            for ticket in tickets_all:
                ticket_ids.append(ticket.ticket_id)

            return ticket_ids