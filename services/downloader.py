import asyncio
import os
import subprocess

import yt_dlp

from aiogram.types import FSInputFile, Message

async def ttdownl(text: str, messageid: str, date: str, message: Message):
    """
    Скачать TikTok-видео и отправить пользователю.
    """
    ydl_opts = {
        'outtmpl': f'{messageid}_{date}.%(ext)s',
        'format': 'mp4',
    }

    def _downs(url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    await asyncio.to_thread(_downs, text, ydl_opts)
    await message.answer_video(video=FSInputFile(f"{messageid}_{date}.mp4"))
    os.remove(f"{messageid}_{date}.mp4")


async def spdownl(text: str, messageid: str, date_str: str, message: Message):
    """
    Скачать Spotify-трек и отправить пользователю.
    """
    folder = f"downloads_{messageid}_{date_str}"
    os.makedirs(folder, exist_ok=True)

    def _sync_download():
        command = ["spotdl", text, "--output", folder]
        subprocess.run(command)

    await asyncio.to_thread(_sync_download)

    files_in_folder = os.listdir(folder)
    for file in files_in_folder:
        file_path = os.path.join(folder, file)
        await message.answer_audio(audio=FSInputFile(file_path))
        os.remove(file_path)
    os.rmdir(folder)
