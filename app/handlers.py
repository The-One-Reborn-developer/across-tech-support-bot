from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F

import app.keyboards as keyboards
import app.database.requests as requests
import app.create_new_ticket as create_new_ticket
import app.find_user_in_db as find_user_in_db
import app.create_new_user_in_db as create_new_user_in_db
import app.get_ticket_status as get_ticket_status
import app.update_ticket as update_ticket

router = Router()

class Request(StatesGroup):
    region = State()
    medical_organization = State()
    name = State()
    position = State()
    phone = State()
    request_type = State()
    request_description = State()

class Ticket(StatesGroup):
    ticket_id = State()
    add_ticket_info_confirmation = State()
    add_ticket_info = State()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await requests.set_user(message.from_user.id)

    content = f"Здравствуйте, {message.from_user.full_name}!\n" \
              f"Я - бот технической поддержки Акросс.\n" \
              f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await message.answer(content, reply_markup=keyboards.main_keyboard())


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    content = f"Пожалуйста, выберите пункт из меню ниже 🔽"
              
    await callback.message.edit_text(content,
                                     reply_markup=keyboards.main_keyboard())


@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery) -> None:
    content = "Телефон тех. поддержки: +78007070572 \n" \
              "Адрес электронной почты: support@across.ru"
    
    await callback.message.edit_text(content,
                                     reply_markup=keyboards.back_to_main_keyboard())


@router.callback_query(F.data == "make_request")
async def make_request(callback: CallbackQuery, state: FSMContext) -> None:
    content = "⚠️ ВНИМАНИЕ ⚠️\nЗаявки на доработку функционала, разработку " \
              "нового функционала, заявки на изменение состава пользователей " \
              "и их настроек доступа, а также на подключение нового " \
              "оборудования можно передать <b>ТОЛЬКО</b> письмом на почту " \
              "support@across.ru"
    
    user_data = await requests.get_user(callback.from_user.id)

    if user_data is None:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=keyboards.confirmation_keyboard())
    elif user_data[0] and user_data[1] and user_data[2] and user_data[3] and user_data[4]:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=keyboards.found_user_confirmation_keyboard())
    else:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=keyboards.confirmation_keyboard())


@router.callback_query(F.data == "further")
async def futher(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Request.region)

    content = "Укажите Ваш регион 🌍🌎🌏 из списка внизу 🔽"

    await callback.message.edit_text(content,
                                     parse_mode="HTML",
                                     reply_markup=keyboards.region_keyboard())


@router.callback_query(Request.region)
async def region_state(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "Belgorod":
        region_data = "Белгородская область"

    await state.update_data({"region": callback.data})
    await requests.update_user(callback.from_user.id, region=region_data)
    await state.set_state(Request.medical_organization)

    content = "Выберите Вашу медицинскую организацию 🏥"

    await callback.message.answer(content,
                                  reply_markup=keyboards.medical_organization_keyboard())


@router.callback_query(Request.medical_organization)
async def organization(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"medical_organization": str(callback.data)})
    await requests.update_user(callback.from_user.id, medical_organization=callback.data)
    await state.set_state(Request.name)

    content = "Напишите Ваше ФИО 🛂"

    await callback.message.answer(content,
                                  reply_markup=keyboards.back_to_main_keyboard())


@router.message(Request.name)
async def name(message: Message, state: FSMContext) -> None:
    await state.update_data({"name": message.text})
    await requests.update_user(message.from_user.id, name=message.text)
    await state.set_state(Request.position)

    content = "Напишите Вашу должность 👨‍⚕️👩‍⚕️"

    await message.answer(content,
                         reply_markup=keyboards.back_to_main_keyboard())


@router.message(Request.position)
async def position(message: Message, state: FSMContext) -> None:
    await state.update_data({"position": message.text})
    await requests.update_user(message.from_user.id, position=message.text)
    await state.set_state(Request.phone)

    content = "Напишите Ваш контактный телефон в формате 9101234567 (без 8 и без +7) 📱"

    await message.answer(content,
                         reply_markup=keyboards.back_to_main_keyboard())


@router.message(Request.phone)
async def phone(message: Message, state: FSMContext) -> None:
    if len(message.text) != 10 or message.text[0] == "+":
        content = "Некорректный номер телефона 🚫"

        return await message.answer(content)
    else:
        await state.update_data({"phone": message.text})
        await requests.update_user(message.from_user.id, phone=message.text)
        await state.set_state(Request.request_type)

        content = "Выберите тип заявки 📝"

        await message.answer(content,
                             reply_markup=keyboards.issue_type_keyboard())
        

@router.callback_query(F.data == "found_user_further")
async def found_user_further(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Request.request_type)

    content = "Выберите тип заявки 📝"

    await callback.message.edit_text(content,
                                     reply_markup=keyboards.issue_type_keyboard())


@router.callback_query(Request.request_type)
async def request_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"request_type": callback.data})
    await state.set_state(Request.request_description)

    if callback.data == "critical":
        content = "Опишите проблему 📝"
    elif callback.data == "no_exchange":
        content = "Опишите проблему и предоставьте ШК ЛИС или ИДМИС 📝"
    elif callback.data == "no_connection":
        content = "Напишите наименование анализатора, ШК ЛИС и предоставьте " \
                  "описание проблемы 📝"
    elif callback.data == "other":
        content = "Подробно опишите Вашу проблему 📝"
        
    await callback.message.answer(content,
                                  reply_markup=keyboards.back_to_main_keyboard())


@router.message(Request.request_description)
async def request_description(message: Message, state: FSMContext) -> None:
    has_photo = False
    chat_id = message.chat.id

    if message.photo:
        message_text = message.caption
        message_photo_id = message.photo[-1].file_id
        has_photo = True
        await message.bot.download(file=message_photo_id, destination=f"app/photos/{message.from_user.id}.jpg")
    else:
        message_text = message.text
        message_photo_id = None

    await state.update_data({"request_description": message_text})

    telegram_id = message.from_user.id
    user_data = await requests.get_user(telegram_id)
    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await message.answer(content)

    user_id = await find_user_in_db.find_user(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket.create_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db.create_user(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket.create_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()

    content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await message.answer(content,
                         reply_markup=keyboards.back_to_main_keyboard())


@router.callback_query(F.data == "request_status")
async def request_status(callback: CallbackQuery, state: FSMContext) -> None:
    tickets = await requests.get_all_user_tickets(callback.from_user.id)

    if tickets:
        await state.set_state(Ticket.ticket_id)
        new_tickets_keyboard = keyboards.tickets_keyboard(tickets)

        content = "Ваши заявки 📝"

        await callback.message.edit_text(content,
                                         reply_markup=new_tickets_keyboard)
    else:
        content = "У Вас нет активных заявок 🙁"

        await callback.message.edit_text(content,
                                         reply_markup=keyboards.back_to_main_keyboard())
        
    
@router.callback_query(Ticket.ticket_id)
async def ticket_id(callback: CallbackQuery, state: FSMContext) -> None:
    
    await state.update_data({"ticket_id": callback.data})

    ticket_status_data = await get_ticket_status.get_ticket_status(int(callback.data))

    if ticket_status_data[0] == 1:
        content = f"Статус Вашей заявки: Выполнена ✅"

        await requests.delete_ticket(int(callback.data))

        await callback.message.edit_text(content,
                                        reply_markup=keyboards.back_to_main_keyboard())
    else:
        content = "Статус Вашей заявки: Не выполнена 🚫\n" \
                 f"Примерное время обработки заявки: {ticket_status_data[1]}\n" \
                 "Хотите добавить информацию к заявке? 📝"
        
        await state.set_state(Ticket.add_ticket_info_confirmation)
        
        await callback.message.edit_text(content,
                                        reply_markup=keyboards.add_ticket_info_keyboard())


@router.callback_query(Ticket.add_ticket_info_confirmation)
async def add_ticket_info(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Ticket.add_ticket_info)

    content = "Напишите информацию к заявке 📝"

    await callback.message.edit_text(content)


@router.message(Ticket.add_ticket_info)
async def add_ticket_info(message: Message, state: FSMContext) -> None:
    await message.answer('Заявка обновляется, подождите ⏳')
    
    ticket_id = await state.get_data()
    ticket_id = ticket_id["ticket_id"]
    user_data = await requests.get_user(message.from_user.id)
    user_phone = user_data[3]

    user_id = await find_user_in_db.find_user(user_phone)

    add_ticket_info_data = await update_ticket.update_ticket(ticket_id, message.text, user_id)

    if add_ticket_info_data == 200:
        content = "Информация добавлена ✅"

        await message.answer(content,
                             reply_markup=keyboards.back_to_main_keyboard())
    else:
        content = "Произошла ошибка при добавлении информации к заявке 🙁\n" \
                  "Попробуйте ещё раз..."

        await message.answer(content,
                             reply_markup=keyboards.back_to_main_keyboard())

@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery) -> None:
    content = "Данная функция пока недоступна 🙁"

    await callback.message.edit_text(content,
                                     reply_markup=keyboards.back_to_main_keyboard())