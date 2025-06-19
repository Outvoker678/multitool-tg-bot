import yt_dlp, os
import asyncio, logging	# импортируем модули asyncio и logging
from tgtoken import TOKEN	# импортируем токен из файла tgtoken
from aiogram import Bot, Dispatcher	# импортируем классы Bot и Dispatcher из aiogram
from aiogram.filters import CommandStart	# импортируем фильтр для команды /start
from aiogram.types import Message, FSInputFile	# импортируем тип Message
from aiogram import F

bot = Bot(TOKEN)	# создаём объект бота с токеном
dp = Dispatcher()	# создаём диспетчер (распределяет входящие обновления)

async def ttdownl(text):
    url = text
    ydl_opts = {
    'outtmpl': 'video.%(ext)s',   # сохраняем файл как 'video.mp4' (расширение подставится)
    'format': 'mp4',}              # просим выбрать формат mp4 (если доступен)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@dp.message(CommandStart())	# регистрируем хендлер на команду /start
async def cmd_start(message: Message):	# асинхронная функция-обработчик
    await message.answer("👋 Привет!\n\n"
        "Я — универсальный бот-инструмент. В будущем я научусь делать многое, "
        "но уже сейчас умею скачивать видео из TikTok без водяных знаков.\n\n"
        "📎 Просто отправь мне ссылку на TikTok-видео, и я скачаю его для тебя!")	# отправляем ответ в чат

@dp.message(F.text) # хендлер срабатывает на любое текстовое сообщение
async def downme(message: Message):	# асинхронная функция-обработчик
    if "tiktok.com" in message.text:
        await message.answer("🔗 Ссылка получена! Сейчас скачаю видео...")
        await ttdownl(message.text)
        await message.answer_video(video=FSInputFile("video.mp4"))        
        os.remove("video.mp4")
        
    else:
        await message.answer("❗️Пожалуйста, отправь ссылку на TikTok-видео.")
	

async def main():	# главная асинхронная функция
    logging.basicConfig(level=logging.INFO)	# настраиваем логирование
    await dp.start_polling(bot)	# запускаем бота через polling (опрос)

if __name__ == '__main__':	# если файл запущен как основная программа
    asyncio.run(main())	# запускаем event loop