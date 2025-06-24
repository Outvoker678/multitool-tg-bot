import yt_dlp, os
import sqlite3
import asyncio, logging
from tgtoken import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
import subprocess

bot = Bot(TOKEN)
dp = Dispatcher()

class Dbfunk():
    def __init__(self):
        self.db = sqlite3.connect('userf.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS TGBOTDB (
            username TEXT,
            tag TEXT)""")
        self.db.commit()
        self.db.close()

    def add(self, user, frend):
        self.db = sqlite3.connect('userf.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(f"INSERT INTO TGBOTDB VALUES ('{user}', '{frend}')")
        self.db.commit()
        self.db.close()
    
dbobjeck = Dbfunk()

maink = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Добавить друга 😊"), KeyboardButton(text="Удалить друга 😢")]], resize_keyboard=True, input_field_placeholder="Выберите пункт меню...")

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

@dp.message(F.text == "Добавить друга 😊")
async def friendo_repost(message: Message):
    await message.answer("Перешлите пожалуйста сообщение от вашего друга.")

@dp.message(F.forward_from)
async def handle_forwarded_message(message: Message):
    forwarded_user_id = message.forward_from.id
    sender_user_id = message.from_user.id
    
    dbobjeck.add(forwarded_user_id, sender_user_id)
    
    await message.answer(
        f"ID пользователя, чье сообщение переслано: {forwarded_user_id}\n"
        f"ID пользователя, который переслал сообщение: {sender_user_id}"
    )

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Привет!\n\n"
        "Я — универсальный бот-инструмент. В будущем я научусь делать многое, "
        "но уже сейчас умею:\n"
        "• скачивать видео из TikTok без водяных знаков\n"
        "• скачивать музыку из Spotify\n"
        "• автоматически пересылать сообщения твоим друзьям\n\n"
        "📎 Просто отправь мне ссылку на TikTok-видео или Spotify-трек, "
        "и я скачаю его для тебя!\n", reply_markup=maink)

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
