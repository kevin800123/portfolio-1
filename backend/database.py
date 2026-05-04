"""SQLite 連線與資料表初始化。"""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "portfolio.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """建立 4 張資料表（若不存在）。"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at    TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT NOT NULL,
            tech_stack  TEXT NOT NULL,
            image_url   TEXT,
            demo_url    TEXT,
            github_url  TEXT,
            created_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL,
            content    TEXT NOT NULL,
            is_read    INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            title      TEXT NOT NULL,
            bio        TEXT NOT NULL,
            avatar_url TEXT,
            email      TEXT,
            github     TEXT,
            linkedin   TEXT,
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("DB OK ->", DB_PATH)
