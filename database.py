import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    chat_title TEXT,
                    sender_id INTEGER,
                    sender_name TEXT,
                    sender_username TEXT,
                    text TEXT,
                    date TEXT NOT NULL,
                    saved_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_id ON messages(chat_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_date ON messages(date)
            """)
            conn.commit()

    def save_message(self, message_id: int, chat_id: int, chat_title: str,
                     sender_id: int, sender_name: str, sender_username: str,
                     text: str, date: datetime):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO messages
                    (message_id, chat_id, chat_title, sender_id, sender_name,
                     sender_username, text, date, saved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                chat_id,
                chat_title,
                sender_id,
                sender_name,
                sender_username,
                text,
                date.isoformat(),
                datetime.utcnow().isoformat(),
            ))
            conn.commit()

    def get_stats(self) -> dict:
        with self._get_conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
            chats = conn.execute(
                "SELECT COUNT(DISTINCT chat_id) FROM messages"
            ).fetchone()[0]
            return {"total_messages": total, "total_chats": chats}
