from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def fourth_media_yes_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='fourth_media_yes'
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