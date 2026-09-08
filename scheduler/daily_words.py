from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models import (
    get_users_by_hour,
    get_new_words_for_user,
    mark_words_sent,
    reset_progress,
    count_words_for_level,
)
from config import WORDS_PER_DAY


async def send_daily_words(bot):
    current_hour = datetime.now().hour
    users = get_users_by_hour(current_hour)

    for user in users:
        telegram_id = user["telegram_id"]
        level = user["level"]

        words = get_new_words_for_user(telegram_id, level, WORDS_PER_DAY)

        # Якщо нових слів не залишилось - учень пройшов весь рівень,
        # починаємо список цього рівня заново
        if not words:
            total = count_words_for_level(level)
            if total > 0:
                reset_progress(telegram_id, level)
                words = get_new_words_for_user(telegram_id, level, WORDS_PER_DAY)
            if not words:
                continue

        text_lines = ["📚 Слова дня:\n"]
        word_ids = []
        for w in words:
            text_lines.append(f"• {w['word']} — {w['translation']}")
            word_ids.append(w["id"])

        try:
            await bot.send_message(telegram_id, "\n".join(text_lines))
            mark_words_sent(telegram_id, word_ids)
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення {telegram_id}: {e}")


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()
    # Перевірка щогодини о :00 - хто обрав цю годину, тому надсилаємо слова
    scheduler.add_job(send_daily_words, "cron", minute=0, args=[bot])
    scheduler.start()
    return scheduler
