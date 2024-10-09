from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def add_ticket_info_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='add_ticket_info'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет ❎',
                    callback_data='main'
                )
            ]
        ]
    )