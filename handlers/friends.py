from aiogram import Router
from aiogram.types import Message
from services.database import dbobjeck
from aiogram import F  

friends_router = Router()

@friends_router.message(F.text == "Добавить друга 😊")
async def friendo_repost(message: Message):
    await message.answer("Перешлите пожалуйста сообщение от вашего друга.")

@friends_router.message(F.forward_from)
async def handle_forwarded_message(message: Message):
    forwarded_user_id = message.forward_from.id
    sender_user_id = message.from_user.id
    
    dbobjeck.add(forwarded_user_id, sender_user_id)
    
    await message.answer(
        f"ID пользователя, чье сообщение переслано: {forwarded_user_id}\n"
        f"ID пользователя, который переслал сообщение: {sender_user_id}"
    )