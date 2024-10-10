from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def second_media_yes_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='second_media_yes'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет ❎\nСоздать заявку с 2 файлами 📸',
                    callback_data='second_media_no'
                )
            ]
        ]
    )