from app.database.models import async_session
from app.database.models import User, Tickets

from sqlalchemy import select


async def set_user(telegram_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)
                await session.commit()


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            data = []

            if user:
                data.append(user.name)
                data.append(user.position)
                data.append(user.region)
                data.append(user.phone)
                data.append(user.medical_organization)
            else:
                return None

            return data
        

async def update_user(telegram_id: int, **kwargs) -> None:
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)

                await session.commit()


async def set_ticket(telegram_id: int, ticket_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            ticket = Tickets(telegram_id=telegram_id, ticket_id=ticket_id)

            session.add(ticket)
            await session.commit()


async def get_all_user_tickets(telegram_id: int) -> list | None:
    async with async_session() as session:
        async with session.begin():
            tickets = await session.scalars(select(Tickets).where(Tickets.telegram_id == telegram_id))

            tickets_all = tickets.all()

            ticket_ids = []

            for ticket in tickets_all:
                ticket_ids.append(ticket.ticket_id)

            return ticket_ids
        

async def delete_ticket(ticket_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            ticket = await session.scalar(select(Tickets).where(Tickets.ticket_id == ticket_id))

            if ticket:
                session.delete(ticket)
                await session.commit()