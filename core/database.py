"""SQLite 错题本"""
import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
DB_PATH = os.path.join(DB_DIR, 'mistakes.db')


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_mistake(topic, question, user_answer, correct_answer):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO mistakes (topic, question, user_answer, correct_answer) VALUES (?,?,?,?)",
        (topic, question, user_answer, correct_answer),
    )
    conn.commit()
    conn.close()


def get_mistakes():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, topic, question, user_answer, correct_answer, created_at "
        "FROM mistakes ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def delete_mistake(mid):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM mistakes WHERE id=?", (mid,))
    conn.commit()
    conn.close()


def clear_all():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM mistakes")
    conn.commit()
    conn.close()