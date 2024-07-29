from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.keyboards import get_main_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    content = f"Здравствуйте, {message.from_user.full_name}!\n" \
              f"Я - бот технической поддержки Акросс.\n" \
              f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await message.answer(content, reply_markup=get_main_keyboard())


@router.callback_query("contacts")
async def contacts(callback: CallbackQuery) -> None:
    pass


@router.callback_query("make_request")
async def make_request(callback: CallbackQuery) -> None:
    pass