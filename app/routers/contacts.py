from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.back_to_main import back_to_main


contacts_router = Router()


@contacts_router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery) -> None:
    content = "Телефон тех. поддержки: +78007070572 \n" \
              "Адрес электронной почты: support@across.ru"

    await callback.message.edit_text(content,
                                     reply_markup=back_to_main())