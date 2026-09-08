from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from config import LEVELS, AVAILABLE_HOURS


def level_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for level in LEVELS:
        builder.button(text=level, callback_data=f"level:{level}")
    builder.adjust(5)
    return builder.as_markup()


def hour_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for hour in AVAILABLE_HOURS:
        builder.button(text=f"{hour}:00", callback_data=f"hour:{hour}")
    builder.adjust(4)
    return builder.as_markup()
