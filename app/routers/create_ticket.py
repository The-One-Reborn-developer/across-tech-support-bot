import shutil
import os

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.back_to_main import back_to_main
from app.keyboards.issue_type import issue_type
from app.keyboards.yes_no import yes_no
from app.keyboards.confirmation import confirmation
from app.keyboards.found_user_confirmation import found_user_confirmation
from app.keyboards.region import region
from app.keyboards.medical_organization import medical_organization
from app.keyboards.first_media_yes_no import first_media_yes_no
from app.keyboards.second_media_yes_no import second_media_yes_no
from app.keyboards.third_media_yes_no import third_media_yes_no
from app.keyboards.fourth_media_yes_no import fourth_media_yes_no

from app.scripts.create_new_ticket import create_new_ticket
from app.scripts.find_user_in_db import find_user_in_db
from app.scripts.create_new_user_in_db import create_new_user_in_db

from app.tasks.celery import get_user_task
from app.tasks.celery import update_user_task


create_ticket_router = Router()


class Request(StatesGroup):
    region = State()
    medical_organization = State()
    name = State()
    position = State()
    phone = State()
    request_type = State()
    request_description = State()
    first_media = State()
    second_media = State()
    third_media = State()
    fourth_media = State()


@create_ticket_router.callback_query(F.data == "make_request")
async def make_request(callback: CallbackQuery, state: FSMContext) -> None:
    content = "⚠️ ВНИМАНИЕ ⚠️\nЗаявки на доработку функционала, разработку " \
              "нового функционала, заявки на изменение состава пользователей " \
              "и их настроек доступа, а также на подключение нового " \
              "оборудования можно передать <b>ТОЛЬКО</b> письмом на почту " \
              "support@across.ru"
    
    result = get_user_task.delay(callback.from_user.id)

    user_data = result.get()

    if user_data is None:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=confirmation())
    elif user_data[0] and user_data[1] and user_data[2] and user_data[3] and user_data[4]:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=found_user_confirmation())
    else:
        await callback.message.edit_text(content, parse_mode="HTML",
                                     reply_markup=confirmation())


@create_ticket_router.callback_query(F.data == "further")
async def futher(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Request.region)

    content = "Укажите Ваш регион 🌍🌎🌏 из списка внизу 🔽"

    await callback.message.edit_text(content,
                                     parse_mode="HTML",
                                     reply_markup=region())


@create_ticket_router.callback_query(Request.region)
async def region_state(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data == "Belgorod":
        region_data = "Белгородская область"

    await state.update_data({"region": callback.data})
    update_user_task.delay(callback.from_user.id, region=region_data)
    await state.set_state(Request.medical_organization)

    content = "Выберите Вашу медицинскую организацию 🏥"

    await callback.message.answer(content,
                                  reply_markup=medical_organization())


@create_ticket_router.callback_query(Request.medical_organization)
async def organization(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"medical_organization": str(callback.data)})
    update_user_task.delay(callback.from_user.id, medical_organization=callback.data)
    await state.set_state(Request.name)

    content = "Напишите Ваше ФИО 🛂"

    await callback.message.answer(content,
                                  reply_markup=back_to_main())


@create_ticket_router.message(Request.name)
async def name(message: Message, state: FSMContext) -> None:
    await state.update_data({"name": message.text})
    update_user_task.delay(message.from_user.id, name=message.text)
    await state.set_state(Request.position)

    content = "Напишите Вашу должность 👨‍⚕️👩‍⚕️"

    await message.answer(content,
                         reply_markup=back_to_main())


@create_ticket_router.message(Request.position)
async def position(message: Message, state: FSMContext) -> None:
    await state.update_data({"position": message.text})
    update_user_task.delay(message.from_user.id, position=message.text)
    await state.set_state(Request.phone)

    content = "Напишите Ваш контактный телефон в формате 9101234567 (без 8 и без +7) 📱"

    await message.answer(content,
                         reply_markup=back_to_main())


@create_ticket_router.message(Request.phone)
async def phone(message: Message, state: FSMContext) -> None:
    if len(message.text) != 10 or message.text[0] == "+":
        content = "Некорректный номер телефона 🚫"

        return await message.answer(content)
    else:
        await state.update_data({"phone": message.text})
        update_user_task.delay(message.from_user.id, phone=message.text)
        await state.set_state(Request.request_type)

        content = "Выберите тип заявки 📝"

        await message.answer(content,
                             reply_markup=issue_type())
        

@create_ticket_router.callback_query(F.data == "found_user_further")
async def found_user_further(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Request.request_type)

    content = "Выберите тип заявки 📝"

    await callback.message.edit_text(content,
                                     reply_markup=issue_type())


@create_ticket_router.callback_query(Request.request_type)
async def request_type(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"request_type": callback.data})
    await state.set_state(Request.first_media)

    try:
        directory_path = f'app/photos/{callback.from_user.id}'
        shutil.rmtree(directory_path)
        print(f"Deleted directory: {directory_path}")
    except OSError as e:
        print(f"Error deleting directory {directory_path}: {e}")

    if callback.data == "critical":
        content = "Опишите проблему 📝, можете прикрепить фото/скриншот 📸\n" \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"
    elif callback.data == "no_exchange":
        content = "Опишите проблему и предоставьте ШК ЛИС или ИДМИС 📝, " \
                  "можете прикрепить фото/скриншот 📸\n" \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"
    elif callback.data == "no_connection":
        content = "Напишите наименование анализатора, ШК ЛИС и предоставьте " \
                  "описание проблемы 📝, можете прикрепить фото/скриншот 📸\n" \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"
    elif callback.data == "other":
        content = "Подробно опишите Вашу проблему 📝, можете прикрепить фото/скриншот 📸\n" \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"
        
    await callback.message.answer(content, parse_mode="HTML",
                                  reply_markup=back_to_main())


@create_ticket_router.message(Request.first_media)
async def first_media(message: Message, state: FSMContext) -> None:
    if message.photo:
        if message.caption is None:
            content = 'Отсутствует описание проблемы 🚫\nПопробуйте ещё раз.'

            return await message.answer(content)
        else:
            await state.update_data({"first_media": 'photo'})
            await state.update_data({"request_description": message.caption})
            message_photo_id = message.photo[-1].file_id

            directory_path = f'app/photos/{message.from_user.id}'
            os.makedirs(directory_path, exist_ok=True)

            await message.bot.download(file=message_photo_id,
                                    destination=f"{directory_path}/{message_photo_id}.jpg")
        
            content = 'Хотите добавить еще одно фото/скриншот?\n' \
                      'Вы сможете позже отправить ещё при добавлении ответа ' \
                      'к заявке.\n' \
                      "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"

            await message.answer(content, parse_mode="HTML",
                                reply_markup=first_media_yes_no())
    else:
        await state.update_data({"request_description": message.text})
        await state.set_state(Request.request_description)

        content = 'Создать заявку?'

        await message.answer(content,
                            reply_markup=yes_no())
        

@create_ticket_router.callback_query(F.data == 'first_media_yes')
async def first_media_yes(callback: CallbackQuery, state: FSMContext) -> None:
    content = 'Отправьте ещё одно фото/скриншот 📸'
    await state.set_state(Request.second_media)
    await callback.message.edit_text(content)


@create_ticket_router.message(Request.second_media)
async def second_media(message: Message) -> None:
    if message.photo:
        message_photo_id = message.photo[-1].file_id

        directory_path = f'app/photos/{message.from_user.id}'
        os.makedirs(directory_path, exist_ok=True)

        await message.bot.download(file=message_photo_id,
                                    destination=f"{directory_path}/{message_photo_id}.jpg")
        
        content = 'Хотите добавить еще одно фото/скриншот?\n' \
                  'Вы сможете позже отправить ещё при добавлении ответа ' \
                  'к заявке.\n' \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"

        await message.answer(content, parse_mode="HTML",
                            reply_markup=second_media_yes_no())
    else:
        content = 'Вы не отправили фото/скриншот 🚫\nПопробуйте ещё раз.'

        await message.answer(content)


@create_ticket_router.callback_query(F.data == 'second_media_yes')
async def second_media_yes(callback: CallbackQuery, state: FSMContext) -> None:
    content = 'Отправьте ещё одно фото/скриншот 📸'
    await state.set_state(Request.third_media)
    await callback.message.edit_text(content)


@create_ticket_router.message(Request.third_media)
async def third_media(message: Message) -> None:
    if message.photo:
        message_photo_id = message.photo[-1].file_id

        directory_path = f'app/photos/{message.from_user.id}'
        os.makedirs(directory_path, exist_ok=True)

        await message.bot.download(file=message_photo_id,
                                    destination=f"{directory_path}/{message_photo_id}.jpg")
        
        content = 'Хотите добавить еще одно фото/скриншот?\n' \
                  'Вы сможете позже отправить ещё при добавлении ответа ' \
                  'к заявке.\n' \
                  "⚠️<b>Внимание</b>⚠️\nОтправляйте только ОДНО фото/скриншот❗"

        await message.answer(content, parse_mode="HTML",
                            reply_markup=third_media_yes_no())
    else:
        content = 'Вы не отправили фото/скриншот 🚫\nПопробуйте ещё раз.'

        await message.answer(content)

    

@create_ticket_router.callback_query(F.data == 'third_media_yes')
async def third_media_yes(callback: CallbackQuery, state: FSMContext) -> None:
    content = 'Отправьте ещё одно фото/скриншот 📸'
    await state.set_state(Request.fourth_media)
    await callback.message.edit_text(content)


@create_ticket_router.message(Request.fourth_media)
async def fourth_media(message: Message) -> None:
    if message.photo:
        message_photo_id = message.photo[-1].file_id

        directory_path = f'app/photos/{message.from_user.id}'
        os.makedirs(directory_path, exist_ok=True)

        await message.bot.download(file=message_photo_id,
                                    destination=f"{directory_path}/{message_photo_id}.jpg")
        
        content = 'Создать заявку?'

        await message.answer(content,
                            reply_markup=fourth_media_yes_no())
    else:
        content = 'Вы не отправили фото/скриншот 🚫\nПопробуйте ещё раз.'

        await message.answer(content)


@create_ticket_router.callback_query(F.data == 'fourth_media_yes')
async def fourth_media_yes(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    telegram_id = callback.from_user.id

    result = get_user_task.delay(telegram_id)

    user_data = result.get()

    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()
    has_photo = True

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await callback.message.edit_text(content)

    user_id = await find_user_in_db(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()
    
    if new_ticket_id is None:
        content = "Ваша заявка не была принята 🙁\nПопробуйте ещё раз."
    else:
        content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await callback.message.answer(content,
                         reply_markup=back_to_main())


@create_ticket_router.callback_query(F.data == "yes_create_ticket")
async def yes_create_ticket(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    telegram_id = callback.from_user.id

    result = get_user_task.delay(telegram_id)

    user_data = result.get()

    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()
    has_photo = False

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await callback.message.edit_text(content)

    user_id = await find_user_in_db(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()
    
    if new_ticket_id is None:
        content = "Ваша заявка не была принята 🙁\nПопробуйте ещё раз."
    else:
        content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await callback.message.answer(content,
                         reply_markup=back_to_main())


@create_ticket_router.callback_query(F.data == "first_media_no")
async def first_media_no(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    telegram_id = callback.from_user.id
    
    result = get_user_task.delay(telegram_id)

    user_data = result.get()

    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()
    has_photo = True

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await callback.message.edit_text(content)

    user_id = await find_user_in_db(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()
    
    if new_ticket_id is None:
        content = "Ваша заявка не была принята 🙁\nПопробуйте ещё раз."
    else:
        content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await callback.message.answer(content,
                         reply_markup=back_to_main())


@create_ticket_router.callback_query(F.data == "second_media_no")
async def second_media_no(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    telegram_id = callback.from_user.id

    result = get_user_task.delay(telegram_id)

    user_data = result.get()

    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()
    has_photo = True

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await callback.message.edit_text(content)

    user_id = await find_user_in_db(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()
    
    if new_ticket_id is None:
        content = "Ваша заявка не была принята 🙁\nПопробуйте ещё раз."
    else:
        content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await callback.message.answer(content,
                         reply_markup=back_to_main())
    

@create_ticket_router.callback_query(F.data == "third_media_no")
async def third_media_no(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id = callback.message.chat.id
    telegram_id = callback.from_user.id

    result = get_user_task.delay(telegram_id)

    user_data = result.get()
    
    user_name = user_data[0]
    user_position = user_data[1]
    user_region = user_data[2]
    user_phone = user_data[3]
    user_medical_organization = user_data[4]
    fsm_user_data = await state.get_data()
    has_photo = True

    content = "Ваша заявка в обработке, ожидайте ⏳"
    await callback.message.edit_text(content)

    user_id = await find_user_in_db(user_phone)

    if user_id:
        print(f'User found. user_id = {user_id}')
        
        new_ticket_id = await create_new_ticket(
            telegram_id,
            user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
    elif user_id is None:
        new_user_id = await create_new_user_in_db(
            user_name,
            user_phone,
            user_medical_organization)

        new_ticket_id = await create_new_ticket(
            telegram_id,
            new_user_id,
            chat_id,
            user_region,
            user_position,
            fsm_user_data["request_type"],
            fsm_user_data["request_description"],
            has_photo)
        
    await state.clear()
    
    if new_ticket_id is None:
        content = "Ваша заявка не была принята 🙁\nПопробуйте ещё раз."
    else:
        content = f"Ваша заявка принята ✅\nНомер заявки {new_ticket_id}"
    await callback.message.answer(content,
                         reply_markup=back_to_main())