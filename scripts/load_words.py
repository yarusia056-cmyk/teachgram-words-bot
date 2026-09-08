import csv
import sys
import os

# Дозволяє запускати скрипт напряму, з коренем проєкту в шляху пошуку
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection, init_db
from config import WORDS_CSV_PATH


def load_words():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    added = 0
    skipped = 0

    with open(WORDS_CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            level = row["level"].strip()
            word = row["word"].strip()
            translation = row["translation"].strip()
            try:
                cur.execute(
                    "INSERT INTO words (level, word, translation) VALUES (?, ?, ?)",
                    (level, word, translation)
                )
                added += 1
            except Exception:
                skipped += 1  # таке слово вже є в базі

    conn.commit()
    conn.close()
    print(f"Додано слів: {added}, пропущено (вже існують): {skipped}")


if __name__ == "__main__":
    load_words()
