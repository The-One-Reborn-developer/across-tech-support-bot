from sqlalchemy import select

from app.database.models.ticket import Ticket
from app.database.models.sync_session import sync_session


async def delete_ticket(ticket_id: int) -> None:
    async with sync_session() as session:
        async with session.begin():
            ticket = await session.scalar(select(Ticket).where(Ticket.ticket_id == ticket_id))

            if ticket:
                await session.delete(ticket)
                await session.commit()