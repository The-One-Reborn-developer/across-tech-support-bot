from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


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


def confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Понятно 👍',
                    callback_data='further'
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


def found_user_confirmation_keyboard() -> InlineKeyboardMarkup:
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
    with open('medical_organizations.txt', 'r') as f:
        medical_organizations = f.read().split('\n')
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=organization,
                    callback_data=str(organization)
                )
            ]
            for organization in medical_organizations
        ]
        + [[
            InlineKeyboardButton(
                text='Назад в главное меню ◀️',
                callback_data='main'
            )
        ]]
    )


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


def tickets_keyboard(ticket_ids: list) -> InlineKeyboardMarkup:
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


def add_ticket_info_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='add_ticket_info'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Нет ❎',
                    callback_data='main'
                )
            ]
        ]
    )


def yes_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да ✅',
                    callback_data='yes_create_ticket'
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


def first_media_yes_no_keyboard() -> InlineKeyboardMarkup:
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


def second_media_yes_no_keyboard() -> InlineKeyboardMarkup:
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


def third_media_yes_no_keyboard() -> InlineKeyboardMarkup:
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


def fourth_media_yes_no_keyboard() -> InlineKeyboardMarkup:
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