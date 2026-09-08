from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from database.models import set_user_level, get_user
from keyboards.inline import level_keyboard, hour_keyboard

router = Router()


@router.message(Command("level"))
async def cmd_level(message: Message):
    await message.answer("Обери свій рівень англійської:", reply_markup=level_keyboard())


@router.callback_query(F.data.startswith("level:"))
async def process_level(callback: CallbackQuery):
    level = callback.data.split(":")[1]
    set_user_level(callback.from_user.id, level)

    user = get_user(callback.from_user.id)

    if user["send_hour"] is None:
        # Перший раз обирає рівень -> одразу питаємо час
        await callback.message.edit_text(f"Рівень встановлено: {level} ✅")
        await callback.message.answer(
            "Тепер обери, о котрій годині щодня надсилати тобі слова:",
            reply_markup=hour_keyboard()
        )
    else:
        await callback.message.edit_text(
            f"Рівень змінено на {level} ✅\n"
            f"Час розсилки залишається: {user['send_hour']}:00"
        )
    await callback.answer()
