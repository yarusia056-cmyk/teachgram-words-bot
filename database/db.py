import sqlite3
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            level TEXT,
            send_hour INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            UNIQUE(level, word, translation)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_words (
            user_id INTEGER,
            word_id INTEGER,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, word_id)
        )
    """)

    conn.commit()
    conn.close()
