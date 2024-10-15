from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
import os
from restaurants import restaurants
from inline_keyboards import get_pagination_keyboard
from aiogram.exceptions import TelegramBadRequest


user_router = Router()
token = os.getenv('TOKEN_BOT')



@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer('Введите команду /restaurants\nЧтобы посмотреть все рестораны')



@user_router.message(StateFilter(default_state), Command('restaurants'))
async def get_restaurants(message: Message):
    current_page = 1

    res, total_count = restaurants, len(restaurants)
    total_pages = (total_count - 1) // 10 + 1
    paginated_restaurants = res[(current_page - 1) * 10: current_page * 10]

    if total_count == 0:
        return await message.answer('Рестораны не найдены')

    await message.answer(
        f'Список ресторанов: \n',
        reply_markup=get_pagination_keyboard(restaurants=paginated_restaurants, current_page=current_page, total_pages=total_pages)
    )



@user_router.callback_query(StateFilter(default_state), F.data.startswith('page_'))
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()
    page = int(callback.data.split("_")[1])
    res, total_count = restaurants, len(restaurants)
    total_pages = (total_count - 1) // 10 + 1
    paginated_restaurants = res[(page - 1) * 10: page * 10]

    if page > 0 and page <= total_pages:
        try:
            await callback.message.edit_text(
                'Список ресторанов: \n',
                reply_markup=get_pagination_keyboard(restaurants=paginated_restaurants, current_page=page, total_pages=total_pages)
            )
        except TelegramBadRequest:
            pass
        



@user_router.callback_query(StateFilter(default_state), F.data.startswith('total_pages'))
async def total_pages(callback: CallbackQuery):
    res = callback.data.split('_')[2]
    await callback.answer(f'Страницы: {res}')


@user_router.callback_query(StateFilter(default_state), F.data.startswith('restaurant_'))
async def get_restaurant(callback: CallbackQuery):
    res = callback.data.split('_')[1]
    restaurant = None
    for i in restaurants:
        if i.id == int(res):
            restaurant = i
    await callback.message.edit_text(text='Информация о ресторане:')
    if not restaurant:
        return await callback.message.answer('Ресторан не найден')
    await callback.message.answer_photo(
        photo=restaurant.photo_url,
        caption=
        f'Название: <b>{restaurant.title}</b>\n\n'
        f'<b>{restaurant.description}</b>\n\n'
        f'Адрес: <b>{restaurant.address}</b>',
    )



@user_router.message(StateFilter(default_state), Command('help'))
async def cmd_help(message: Message):
    await message.answer('Все команды:\n/start\n/restaurants\n')
    

@user_router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.answer(
            'Неизвестная команда\nВведите /help - чтобы посмотреть доступные команды'
    )
