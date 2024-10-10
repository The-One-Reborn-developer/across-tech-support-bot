from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def tickets(ticket_ids: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'🔍 {ticket_id}',
                    callback_data=str(ticket_id)
                )
            ]
            for ticket_id in ticket_ids
        ]
        + [[
            InlineKeyboardButton(
                text='Назад в главное меню ◀️',
                callback_data='main'
            )
        ]]
    )