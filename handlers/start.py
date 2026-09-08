from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.models import add_or_get_user
from keyboards.inline import level_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    add_or_get_user(message.from_user.id)
    await message.answer(
        "Привіт! 👋 Я допоможу тобі вивчати англійські слова щодня.\n\n"
        "Спочатку обери свій рівень англійської:",
        reply_markup=level_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступні команди:\n"
        "/start — почати роботу з ботом\n"
        "/level — змінити рівень англійської\n"
        "/time — змінити час щоденної розсилки\n"
        "/progress — подивитись прогрес\n"
        "/help — це повідомлення"
    )
