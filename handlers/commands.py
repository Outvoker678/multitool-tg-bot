from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards.start_keyboard import start_keyboard

commands_router = Router()


@commands_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я — универсальный бот-инструмент. "
        "Чтобы узнать, что я умею, воспользуйся командой /help.",
        reply_markup=start_keyboard,
    )

@commands_router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(
        "🛠 Я умею:\n"
        "• Скачивать видео из TikTok\n"
        "• Скачивать музыку из Spotify\n"
        "\n"
        "⚙️ В разработке: добавление друзей для автоматической отправки."
    )
