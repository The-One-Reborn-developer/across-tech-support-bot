from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def back_to_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Назад в главное меню ◀️',
                    callback_data='main'
                )
            ]
        ]
    )