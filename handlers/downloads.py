import asyncio, os
from aiogram.types import FSInputFile, Message
from aiogram import Router, F

from aiogram import F  # замените строку from aiogram.filters import F на этот импорт
import yt_dlp
import subprocess
from services.downloader import spdownl, ttdownl

downloads_router = Router()


@downloads_router.message(F.text)
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