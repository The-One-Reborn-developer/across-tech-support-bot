import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

from app.routers.main import main_router
from app.routers.contacts import contacts_router
from app.routers.faq import faq_router
from app.routers.ticket_status import ticket_status_router
from app.routers.create_ticket import create_ticket_router

from app.tasks.celery import create_database_tables_task


async def main() -> None:
    create_database_tables_task.delay()

    load_dotenv(find_dotenv())

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_routers(main_router, contacts_router, faq_router, ticket_status_router, create_ticket_router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())