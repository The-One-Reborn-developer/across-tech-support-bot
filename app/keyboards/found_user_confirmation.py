from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def found_user_confirmation() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Понятно 👍👍',
                    callback_data='found_user_further'
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