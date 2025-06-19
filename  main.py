import asyncio, logging	# импортируем модули asyncio и logging
from tgtoken import TOKEN	# импортируем токен из файла tgtoken
from aiogram import Bot, Dispatcher	# импортируем классы Bot и Dispatcher из aiogram
from aiogram.filters import CommandStart	# импортируем фильтр для команды /start
from aiogram.types import Message	# импортируем тип Message

bot = Bot(TOKEN)	# создаём объект бота с токеном
dp = Dispatcher()	# создаём диспетчер (распределяет входящие обновления)

@dp.message(CommandStart())	# регистрируем хендлер на команду /start
async def cmd_start(message: Message):	# асинхронная функция-обработчик
    await message.answer('Привет!')	# отправляем ответ в чат

async def main():	# главная асинхронная функция
    logging.basicConfig(level=logging.INFO)	# настраиваем логирование
    await dp.start_polling(bot)	# запускаем бота через polling (опрос)

if __name__ == '__main__':	# если файл запущен как основная программа
    asyncio.run(main())	# запускаем event loop