import logging
import asyncio

from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN
from handlers.friends import friends_router
from handlers.commands import commands_router
from handlers.downloads import downloads_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main():
    """
    Запуск polling и настройка логирования.
    """
    dp.include_router(friends_router)
    dp.include_router(commands_router)
    dp.include_router(downloads_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
