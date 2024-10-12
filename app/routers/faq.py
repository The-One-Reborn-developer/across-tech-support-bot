import re

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards.back_to_main import back_to_main
from app.keyboards.articles import articles

from app.scripts.get_knowledge_base_articles import get_knowledge_base_articles
from app.scripts.get_knowledge_base_articles_page import get_knowledge_base_articles_page
from app.scripts.get_article import get_article


faq_router = Router()


class KnowledgeBase(StatesGroup):
    article_selection = State()


def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


@faq_router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery, state: FSMContext) -> None:
    data = await get_knowledge_base_articles()
    total_pages = data['pagination']['total_pages']

    with open('app/temp/articles_data.txt', 'w', encoding='utf-8') as file:
        file.write("")

    if total_pages > 1:
        for page in range(1, total_pages + 1):
            data = await get_knowledge_base_articles_page(page)
            articles_data = data['data']

            for article_id, article_info in articles_data.items():
                with open('app/temp/articles_data.txt', 'a', encoding='utf-8') as file:
                    file.write(f"{article_id},{article_info['title']['ru'].rstrip('.,!?')}\n")
    else:
        articles_data = data['data']

        with open('app/temp/articles_data.txt', 'a', encoding='utf-8') as file:
            for article_id, article_info in articles_data.items():
                file.write(f"{article_id},{article_info['title']['ru'].rstrip('.,!?')}\n")

    content = "Выберите интересующую Вас статью 📖"
    
    await state.set_state(KnowledgeBase.article_selection)

    await callback.message.edit_text(content,
                                     reply_markup=articles())


@faq_router.callback_query(KnowledgeBase.article_selection)
async def article_selection(callback: CallbackQuery, state: FSMContext) -> None:
    article_id = callback.data

    data = await get_article(article_id)

    content = data['data']['body']['ru']
    edited_content = strip_html_tags(content)

    await callback.message.edit_text(edited_content, 
                                     reply_markup=back_to_main())