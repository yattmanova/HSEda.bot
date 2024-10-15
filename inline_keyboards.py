from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_pagination_keyboard(restaurants, current_page, total_pages):
    kb_builder = InlineKeyboardBuilder()
    for establishment in restaurants:
        kb_builder.row(InlineKeyboardButton(text=f'{establishment.title}', callback_data=f'restaurant_{establishment.id}'), width=1)
    kb_builder.row(
        InlineKeyboardButton(
            text='<<<',
            callback_data=f'page_{current_page - 1}' if current_page > 1 else 'page_1'
        ),
        InlineKeyboardButton(
            text=f'{current_page}/{total_pages}',
            callback_data=f'total_pages_{current_page}/{total_pages}',
        ),
        InlineKeyboardButton(
            text='>>>',
            callback_data=f'page_{current_page + 1}' if current_page < total_pages else f'page_{total_pages}'
        ),
        width=3
    )
    return kb_builder.as_markup()