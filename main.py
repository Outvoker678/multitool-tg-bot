import yt_dlp, os
import asyncio, logging
from tgtoken import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram import F
import subprocess

bot = Bot(TOKEN)
dp = Dispatcher()

async def ttdownl(text, messageid, date, message):  # Скачать TikTok-видео
    ydl_opts = {
        'outtmpl': f'{messageid}_{date}.%(ext)s',
        'format': 'mp4',
    }
    def downs(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    await asyncio.to_thread(downs, text, ydl_opts)
    await message.answer_video(video=FSInputFile(f"{messageid}_{date}.mp4"))
    os.remove(f"{messageid}_{date}.mp4")

async def spdownl(text, messageid, date_str, message: Message):  # Скачать Spotify-трек
    folder = f"downloads_{messageid}_{date_str}"
    os.makedirs(folder, exist_ok=True)

    def sync_download():
        command = ["spotdl", text, "--output", folder]
        subprocess.run(command)

    await asyncio.to_thread(sync_download)

    filesp = os.listdir(folder)
    for files in filesp:
        await message.answer_audio(audio=FSInputFile(os.path.join(folder, files)))
        os.remove(os.path.join(folder, files))
    os.rmdir(folder)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Привет!\n\n"
        "Я — универсальный бот-инструмент. В будущем я научусь делать многое, "
        "но уже сейчас умею:\n"
        "• скачивать видео из TikTok без водяных знаков\n"
        "• скачивать музыку из Spotify\n\n"
        "📎 Просто отправь мне ссылку на TikTok-видео или Spotify-трек, и я скачаю его для тебя!")

@dp.message(F.text)
async def downme(message: Message):
    date_str = message.date.strftime("%Y%m%d_%H%M%S")  # преобразуем дату в строку
    if "tiktok.com" in message.text:
        await message.answer("🔗 Ссылка получена! Сейчас скачаю видео...")
        await ttdownl(message.text, message.message_id, date_str, message)
    elif "open.spotify.com" in message.text:
        await message.answer("🔗 Ссылка получена! Сейчас скачаю трек...")
        await spdownl(message.text, message.message_id, date_str, message)
    else:
        await message.answer("❗️Пожалуйста, отправь ссылку на TikTok или Spotify.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
