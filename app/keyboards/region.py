from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def region() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Белгородская область 🇷🇺',
                    callback_data='Belgorod'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Назад в главное меню ◀️',
                    callback_data='main'
                )
            ]
        ]
    )