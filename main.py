import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher


async def main():
    load_dotenv(find_dotenv())

    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())