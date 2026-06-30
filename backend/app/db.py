import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("MYNOTES_DB_PATH", "data/mynotes.db"))


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_events (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          kind TEXT NOT NULL,
          payload TEXT NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn


def save_event(kind: str, payload: str) -> None:
    with get_conn() as conn:
        conn.execute("INSERT INTO ai_events(kind, payload) VALUES (?, ?)", (kind, payload))
