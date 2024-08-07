from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

from app.keyboards import (main_keyboard,
                           back_to_main_keyboard,
                           region_keyboard,
                           medical_organization_keyboard,
                           issue_type_keyboard)

import app.database.requests as requests

router = Router()

class Request(StatesGroup):
    region = State()
    organization = State()
    name = State()
    position = State()
    phone = State()
    request_type = State()
    request_description = State()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await requests.set_user(message.from_user.id)

    content = f"Здравствуйте, {message.from_user.full_name}!\n" \
              f"Я - бот технической поддержки Акросс.\n" \
              f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await message.answer(content, reply_markup=main_keyboard())


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    content = f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await callback.message.edit_text(content, reply_markup=main_keyboard())


@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery) -> None:
    content = "Телефон тех. поддержки: +78007070572 \n" \
              "Адрес электронной почты: support@across.ru"
    
    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "make_request")
async def make_request(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Request.region)

    content = "⚠️ ВНИМАНИЕ ⚠️\nЗаявки на доработку функционала, разработку " \
              "нового функционала, заявки на изменение состава пользователей " \
              "и их настроек доступа, а также на подключение нового " \
              "оборудования можно передать <b>ТОЛЬКО</b> письмом на почту " \
              "support@across.ru\n\n" \
              "Укажите Ваш регион 🌍🌎🌏 из списка внизу 🔽"

    await callback.message.edit_text(content,
                                     parse_mode="HTML",
                                     reply_markup=region_keyboard())
    

@router.callback_query(Request.region)
async def region_state(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"region": callback.data})
    await state.set_state(Request.organization)

    content = "Выберите Вашу медицинскую организацию 🏥"

    await callback.message.answer(content, reply_markup=medical_organization_keyboard())


@router.callback_query(Request.organization)
async def organization(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"organization": callback.data})
    await state.set_state(Request.name)

    content = "Напишите Ваше ФИО 🛂"

    await callback.message.answer(content, reply_markup=back_to_main_keyboard())


@router.message(Request.name)
async def name(message: Message, state: FSMContext) -> None:
    await state.update_data({"name": message.text})
    await state.set_state(Request.position)

    content = "Напишите Вашу должность 👨‍⚕️👩‍⚕️"

    await message.answer(content, reply_markup=back_to_main_keyboard())


@router.message(Request.position)
async def position(message: Message, state: FSMContext) -> None:
    await state.update_data({"position": message.text})
    await state.set_state(Request.phone)

    content = "Напишите Ваш контактный телефон 📱"

    await message.answer(content, reply_markup=back_to_main_keyboard())


@router.message(Request.phone)
async def phone(message: Message, state: FSMContext) -> None:
    if len(message.text) != 11:
        content = "Некорректный номер телефона 🚫\n"

        return await message.answer(content)
    else:
        await state.update_data({"phone": message.text})
        await state.set_state(Request.request_type)

        content = "Выберите тип заявки 📝"

        await message.answer(content, reply_markup=issue_type_keyboard())


@router.callback_query(Request.request_type)
async def request_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"request_type": callback.data})
    await state.set_state(Request.request_description)

    if callback.data == "critical":
        content = "Опишите проблему 📝"
    elif callback.data == "no_exchange":
        content = "Опишите проблему 📝 и предоставьте ШК ЛИС или ИДМИС"
    elif callback.data == "no_connection":
        content = "Напишите наименование анализатора, ШК ЛИС и предоставьте " \
                  "описание проблемы 📝"
    elif callback.data == "other":
        content = "Подробно опишите Вашу проблему 📝"
        
    await callback.message.answer(content, reply_markup=back_to_main_keyboard())


@router.message(Request.request_description)
async def request_description(message: Message, state: FSMContext) -> None:
    message_content = message.photo if message.photo else message.text
    await state.update_data({"request_description": message_content})

    content = "Ваша заявка принята ✅"

    await state.clear()

    await message.answer(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "request_status")
async def request_status(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())


@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content, reply_markup=back_to_main_keyboard())