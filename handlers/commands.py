from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.models import get_user, count_words_for_level, count_sent_words

router = Router()


@router.message(Command("progress"))
async def cmd_progress(message: Message):
    user = get_user(message.from_user.id)

    if not user or not user["level"]:
        await message.answer("Спочатку обери рівень командою /level")
        return

    total = count_words_for_level(user["level"])
    sent = count_sent_words(message.from_user.id, user["level"])

    time_line = f"{user['send_hour']}:00" if user["send_hour"] is not None else "ще не обрано (/time)"

    await message.answer(
        f"Рівень: {user['level']}\n"
        f"Вивчено слів: {sent} з {total}\n"
        f"Час розсилки: {time_line}"
    )
