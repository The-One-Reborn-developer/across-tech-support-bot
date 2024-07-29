from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.keyboards import get_main_keyboard, back_to_main_keyboard

router = Router()

class Request(StatesGroup):
    region = State()
    organization = State()
    lab = State()
    name = State()
    position = State()
    email = State()
    phone = State()
    request_type = State()
    request_description = State()


@router.message(CommandStart())
async def start(message: Message) -> None:
    content = f"Здравствуйте, {message.from_user.full_name}!\n" \
              f"Я - бот технической поддержки Акросс.\n" \
              f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await message.answer(content, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery) -> None:
    content = f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await callback.message.edit_text(content, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery) -> None:
    content = "Телефон тех. поддержки: +78007070572 \n" \
              "Адрес электронной почты: support@across.ru"
    
    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "make_request")
async def make_request(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "request_status")
async def request_status(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())