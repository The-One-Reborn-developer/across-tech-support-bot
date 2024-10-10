from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def issue_type() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Критическая ошибка ЛИС',
                    callback_data='critical'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет обмена с МИС',
                    callback_data='no_exchange'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет связи с анализаторами',
                    callback_data='no_connection'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Другое',
                    callback_data='other'
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