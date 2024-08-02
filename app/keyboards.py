from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)
import urllib.parse


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
                    text='Назад в главное меню ◀️',
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
            ],
            [
                InlineKeyboardButton(
                    text='Назад в главное меню ◀️',
                    callback_data='main'
                )
            ]
        ]
    )


def medical_organization_keyboard() -> InlineKeyboardMarkup:
    # TODO
    pass
    

def issue_type_keyboard() -> InlineKeyboardMarkup:
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