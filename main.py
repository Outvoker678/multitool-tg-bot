import yt_dlp, os	# импортируем модули для скачивания видео и работы с файлами
import asyncio, logging	# импортируем модули для асинхронного программирования и логирования
from tgtoken import TOKEN	# импортируем токен бота из файла tgtoken
from aiogram import Bot, Dispatcher	# импортируем классы Bot и Dispatcher из aiogram
from aiogram.filters import CommandStart	# импортируем фильтр для команды /start
from aiogram.types import Message, FSInputFile	# импортируем типы Message и FSInputFile
from aiogram import F	# импортируем вспомогательный модуль F из aiogram

bot = Bot(TOKEN)	# создаём объект бота с токеном
dp = Dispatcher()	# создаём объект диспетчера для обработки сообщений

async def ttdownl(text, messageid, date):	# асинхронная функция для скачивания видео
    ydl_opts = {	# создаём словарь с настройками для yt_dlp
        'outtmpl': f'{messageid}_{date}.%(ext)s',   # шаблон имени выходного файла
        'format': 'mp4',                            # формат скачиваемого видео
    }
    def downs(url, ydl_opts):	# функция для скачивания видео через yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:	# создаём объект YoutubeDL с настройками
            ydl.download([url])	# скачиваем видео по ссылке
    await asyncio.to_thread(downs, text, ydl_opts)	# запускаем скачивание в отдельном потоке

@dp.message(CommandStart())	# регистрируем хендлер на команду /start
async def cmd_start(message: Message):	# асинхронная функция-обработчик команды /start
    await message.answer("👋 Привет!\n\n"
        "Я — универсальный бот-инструмент. В будущем я научусь делать многое, "
        "но уже сейчас умею скачивать видео из TikTok без водяных знаков.\n\n"
        "📎 Просто отправь мне ссылку на TikTok-видео, и я скачаю его для тебя!")	# отправляем приветственное сообщение

@dp.message(F.text)	# регистрируем хендлер на любое текстовое сообщение
async def downme(message: Message):	# асинхронная функция-обработчик текстовых сообщений
    if "tiktok.com" in message.text:	# если в сообщении есть ссылка на tiktok.com
        await message.answer("🔗 Ссылка получена! Сейчас скачаю видео...")	# отправляем уведомление о начале скачивания
        await ttdownl(message.text, message.message_id, message.date)	# скачиваем видео по ссылке
        await message.answer_video(video=FSInputFile(f"{message.message_id}_{message.date}.mp4"))	# отправляем скачанное видео пользователю
        os.remove(f"{message.message_id}_{message.date}.mp4")	# удаляем видеофайл после отправки
    else:	# если ссылка не найдена
        await message.answer("❗️Пожалуйста, отправь ссылку на TikTok-видео.")	# просим пользователя отправить корректную ссылку

async def main():	# главная асинхронная функция
    logging.basicConfig(level=logging.INFO)	# настраиваем уровень логирования
    await dp.start_polling(bot)	# запускаем polling для обработки сообщений

if __name__ == '__main__':	# если файл запущен как основная программа
    asyncio.run(main())	# запускаем главный event loop
