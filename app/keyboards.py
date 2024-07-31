from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Контакты тех. поддержки 📞',
                    callback_data='contacts'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Оставить заявку 📝',
                    callback_data='make_request'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Узнать статус заявки 🔎',
                    callback_data='request_status'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Часто задаваемые вопросы ❓',
                    callback_data='faq'
                )
            ]
        ]
    )


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Назад ◀️',
                    callback_data='main'
                )
            ]
        ]
    )


def region_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Белгородская область 🇷🇺',
                    callback_data='Belgorod'
                )
            ]            
        ]
    )