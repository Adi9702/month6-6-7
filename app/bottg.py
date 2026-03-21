from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.bot_setup import django
from app.users.models import TelegramLinkCode, User
from asgiref.sync import sync_to_async

router = Router()

@sync_to_async
def link_user_chat(code: str, chat_id: int) -> bool:
    obj = (
        TelegramLinkCode.objects
        .select_related("user")
        .filter(code=code, is_user=False)
        .first()
    )

    if obj is None:
        return False

    user = obj.user
    user.telegram_chat_id = chat_id
    user.save(update_fields=["telegram_chat_id"])

    obj.is_user = True
    obj.save(update_fields=["is_user"])
    return True

@router.message(Command("link"))
async def link(message:Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        return await message.answer("\link 123123")

    code = parts[1].strip()

    ok = await link_user_chat(code, message.chat.id)
    if not ok:
        return await message.answer("Error Code")

    await message.answer("Welcome")