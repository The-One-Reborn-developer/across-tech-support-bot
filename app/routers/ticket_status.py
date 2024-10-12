import shutil
import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.back_to_main import back_to_main
import app.keyboards.tickets as tickets_keyboard
from app.keyboards.add_ticket_info import add_ticket_info_keyboard

from app.scripts.get_ticket_status import get_ticket_status
from app.scripts.find_user_in_db import find_user_in_db
from app.scripts.update_ticket import update_ticket

from app.tasks.celery import get_all_user_tickets_task
from app.tasks.celery import delete_ticket_task
from app.tasks.celery import get_user_task


ticket_status_router = Router()


class Ticket(StatesGroup):
    ticket_id = State()
    add_ticket_info_confirmation = State()
    add_ticket_info = State()


@ticket_status_router.callback_query(F.data == "request_status")
async def request_status(callback: CallbackQuery, state: FSMContext) -> None:
    result = get_all_user_tickets_task.delay(callback.from_user.id)

    tickets = result.get()

    if tickets:
        await state.set_state(Ticket.ticket_id)
        new_tickets_keyboard = tickets_keyboard.tickets(tickets)

        content = "Ваши заявки 📝"

        await callback.message.edit_text(content,
                                         reply_markup=new_tickets_keyboard)
    else:
        content = "У Вас нет активных заявок 🤔"

        await callback.message.edit_text(content,
                                         reply_markup=back_to_main())
        
    
@ticket_status_router.callback_query(Ticket.ticket_id)
async def ticket_id(callback: CallbackQuery, state: FSMContext) -> None:
    
    await state.update_data({"ticket_id": callback.data})

    ticket_status_data = await get_ticket_status(int(callback.data))

    if ticket_status_data[0] == 1:
        content = f"Статус Вашей заявки: Выполнена ✅"

        delete_ticket_task.delay(int(callback.data))

        await callback.message.edit_text(content,
                                        reply_markup=back_to_main())
    else:
        content = "Статус Вашей заявки: Не выполнена 🚫\n" \
                 f"Примерное время обработки заявки: {ticket_status_data[1]}\n" \
                 "Хотите добавить информацию к заявке? 📝"
        
        await state.set_state(Ticket.add_ticket_info_confirmation)
        
        await callback.message.edit_text(content,
                                        reply_markup=add_ticket_info_keyboard())


@ticket_status_router.callback_query(Ticket.add_ticket_info_confirmation)
async def add_ticket_info(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Ticket.add_ticket_info)

    try:
        directory_path = f'app/photos/{callback.from_user.id}'
        shutil.rmtree(directory_path)
        print(f"Deleted directory: {directory_path}")
    except OSError as e:
        print(f"Error deleting directory {directory_path}: {e}")

    content = "Напишите информацию к заявке 📝, можете прикрепить одно фото/скриншот 📸"

    await callback.message.edit_text(content)


@ticket_status_router.message(Ticket.add_ticket_info)
async def add_ticket_info(message: Message, state: FSMContext) -> None:
    has_photo = False
    message_text = ''

    if message.photo:
        if message.caption is None:
            content = 'Отсутствует описание проблемы 🚫\nПопробуйте ещё раз.'

            return await message.answer(content)
        else:
            has_photo = True
            message_text = message.caption

            message_photo_id = message.photo[-1].file_id

            directory_path = f'app/photos/{message.from_user.id}'
            os.makedirs(directory_path, exist_ok=True)

            await message.bot.download(file=message_photo_id,
                                    destination=f"{directory_path}/{message_photo_id}.jpg")
    else:
        message_text = message.text
    
    await message.answer('Заявка обновляется, подождите ⏳')
    
    ticket_id = await state.get_data()
    ticket_id = ticket_id["ticket_id"]

    result = get_user_task.delay(message.from_user.id)

    user_data = result.get()

    user_phone = user_data[3]

    user_id = await find_user_in_db(user_phone)

    add_ticket_info_data = await update_ticket(ticket_id,
                                               message_text,
                                               user_id,
                                               has_photo,
                                               message.from_user.id)

    if add_ticket_info_data == 200:
        content = "Информация добавлена ✅"

        await message.answer(content,
                             reply_markup=back_to_main())
    else:
        content = "Произошла ошибка при добавлении информации к заявке 🙁\n" \
                  "Попробуйте ещё раз..."

        await message.answer(content,
                             reply_markup=back_to_main())