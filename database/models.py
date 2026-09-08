from database.db import get_connection


def add_or_get_user(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()
    if user is None:
        cur.execute("INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cur.fetchone()
    conn.close()
    return user


def get_user(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()
    conn.close()
    return user


def set_user_level(telegram_id: int, level: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET level = ? WHERE telegram_id = ?", (level, telegram_id))
    conn.commit()
    conn.close()


def set_user_hour(telegram_id: int, hour: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET send_hour = ? WHERE telegram_id = ?", (hour, telegram_id))
    conn.commit()
    conn.close()


def get_users_by_hour(hour: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE send_hour = ? AND level IS NOT NULL",
        (hour,)
    )
    users = cur.fetchall()
    conn.close()
    return users


def get_new_words_for_user(telegram_id: int, level: str, count: int = 3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT w.* FROM words w
        WHERE w.level = ?
          AND w.id NOT IN (
              SELECT word_id FROM sent_words WHERE user_id = ?
          )
        ORDER BY RANDOM()
        LIMIT ?
    """, (level, telegram_id, count))
    words = cur.fetchall()
    conn.close()
    return words


def mark_words_sent(telegram_id: int, word_ids):
    if not word_ids:
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO sent_words (user_id, word_id) VALUES (?, ?)",
        [(telegram_id, wid) for wid in word_ids]
    )
    conn.commit()
    conn.close()


def count_words_for_level(level: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM words WHERE level = ?", (level,))
    count = cur.fetchone()[0]
    conn.close()
    return count


def count_sent_words(telegram_id: int, level: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM sent_words sw
        JOIN words w ON sw.word_id = w.id
        WHERE sw.user_id = ? AND w.level = ?
    """, (telegram_id, level))
    count = cur.fetchone()[0]
    conn.close()
    return count


def reset_progress(telegram_id: int, level: str):
    """Викликається, коли учень пройшов усі слова рівня - починаємо список заново."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM sent_words
        WHERE user_id = ? AND word_id IN (
            SELECT id FROM words WHERE level = ?
        )
    """, (telegram_id, level))
    conn.commit()
    conn.close()
