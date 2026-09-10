from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from database.models import add_or_get_user, set_user_hour, get_user
from keyboards.inline import hour_keyboard

router = Router()


@router.message(Command("time"))
async def cmd_time(message: Message):
    await message.answer(
        "Обери зручний час для щоденної розсилки:",
        reply_markup=hour_keyboard()
    )


@router.callback_query(F.data.startswith("hour:"))
async def process_hour(callback: CallbackQuery):
    hour = int(callback.data.split(":")[1])
    telegram_id = callback.from_user.id

    # Переконуємося, що користувач є в базі
    add_or_get_user(telegram_id)

    # Зберігаємо обраний час
    set_user_hour(telegram_id, hour)

    # Отримуємо актуальні дані користувача
    user = get_user(telegram_id)

    if user and user["level"]:
        await callback.message.edit_text(
            f"Час встановлено: {hour}:00 ✅\n\n"
            f"Усе готово! Щодня о {hour}:00 ти отримуватимеш "
            f"3 нових слова рівня {user['level']}.\n\n"
            "Змінити рівень: /level\n"
            "Змінити час: /time"
        )
    else:
        await callback.message.edit_text(
            f"Час встановлено: {hour}:00 ✅\n\n"
            "Тепер обери свій рівень: /level"
        )

    await callback.answer()