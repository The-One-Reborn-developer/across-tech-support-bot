from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def third_media_yes_no() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='third_media_yes'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет ❎\nСоздать заявку с 3 файлами 📸',
                    callback_data='third_media_no'
                )
            ]
        ]
    )