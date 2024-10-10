from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def first_media_yes_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='first_media_yes'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет ❎\nСоздать заявку с 1 файлом 📸',
                    callback_data='first_media_no'
                )
            ]
        ]
    )