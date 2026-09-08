import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database.db import init_db
from handlers import start, level, time_setting, commands
from scheduler.daily_words import setup_scheduler

logging.basicConfig(level=logging.INFO)


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(level.router)
    dp.include_router(time_setting.router)
    dp.include_router(commands.router)

    setup_scheduler(bot)

    print("Бот запущено...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
