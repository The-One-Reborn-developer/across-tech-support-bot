import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.routers.contacts import contacts_router
from app.routers.faq import faq_router
from app.routers.ticket_status import ticket_status_router

from app.database.models import async_main


async def main() -> None:
    await async_main()
    load_dotenv(find_dotenv())

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_routers(router, contacts_router, faq_router, ticket_status_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())