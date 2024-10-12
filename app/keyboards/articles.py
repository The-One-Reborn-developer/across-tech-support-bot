from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)


def articles() -> InlineKeyboardMarkup:
    articles_id = []
    articles_title = []

    with open('app/temp/articles_data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # Ensure the line contains a comma to split
            if ',' in line:
                article_id, article_title = line.split(',', 1)  # Split only once in case the title contains commas
                article_title = article_title.strip()

                articles_id.append(article_id)
                articles_title.append(article_title)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=article_title,
                    callback_data=str(article_id)
                )
            ]
            for article_id, article_title in zip(articles_id, articles_title)
        ]
        + [[
            InlineKeyboardButton(
                text='Назад в главное меню ◀️',
                callback_data='main'
            )
        ]]
    )