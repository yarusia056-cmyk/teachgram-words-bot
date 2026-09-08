import os

# Встав свій токен від BotFather сюди АБО задай змінну середовища BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "words_bot.db")
WORDS_CSV_PATH = os.path.join(BASE_DIR, "data", "words.csv")

LEVELS = ["A1", "A2", "B1", "B2", "C1"]
AVAILABLE_HOURS = list(range(8, 23))  # обрати можна час з 8:00 до 22:00
WORDS_PER_DAY = 3
