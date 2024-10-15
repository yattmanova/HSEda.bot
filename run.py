from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from user_handlers import user_router
import os
import asyncio
import logging




async def main():
    # session: AiohttpSession = AiohttpSession(proxy='http://proxy.server:3128') #pythonanywhere
    #TOKEN_BOT = os.getenv('TOKEN_BOT')
    TOKEN_BOT = '7575453212:AAFgTeoL6650jRmY9bHB8_UA12iztszK0TM'
    bot = Bot(token=TOKEN_BOT, parse_mode=ParseMode.HTML)

    await bot.delete_webhook(True)
    dp = Dispatcher()
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Остановка бота')
