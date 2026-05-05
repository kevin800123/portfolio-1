"""資料庫連線與初始化（PostgreSQL / SQLite 雙引擎）。

行為：
- 若環境變數 DATABASE_URL 設定為 postgres://... 或 postgresql://...，就連線 PostgreSQL
  （透過 psycopg2），這對應 Supabase / Render / Heroku 等雲端服務。
- 否則退回本地 SQLite（檔案 backend/portfolio.db），方便本地開發。

注意：所有路由都呼叫 get_db().execute(sql, params)，sql 一律用 ? 佔位符；本模組會在
PostgreSQL 模式下自動把 ? 轉成 %s（psycopg2 用的格式）。
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import suppress
from pathlib import Path
from typing import Any, Iterable, Sequence

with suppress(ImportError):
    # 本地讀取 .env；雲端平台（Render / Railway / Fly.io）會直接注入環境變數
    from dotenv import load_dotenv

    load_dotenv()

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()
USE_POSTGRES = DATABASE_URL.startswith(("postgres://", "postgresql://"))

# ---- PostgreSQL 模式：lazy import 避免本地開發時必須安裝 psycopg2 ----
if USE_POSTGRES:
    import psycopg2  # type: ignore
    import psycopg2.extras  # type: ignore

SQLITE_PATH = Path(__file__).parent / "portfolio.db"


class DBConnection:
    """跨資料庫的連線包裝。

    - 對外維持 sqlite3 風格 API：execute / executemany / commit / close
    - SQL 一律用 ? 佔位符，PostgreSQL 模式時自動替換為 %s
    - fetchone / fetchall 回傳 dict-like（PG 用 RealDictCursor、SQLite 用 Row）
    """

    def __init__(self) -> None:
        self.use_pg = USE_POSTGRES
        if USE_POSTGRES:
            self._conn = psycopg2.connect(DATABASE_URL)
        else:
            self._conn = sqlite3.connect(SQLITE_PATH)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")

    def _cursor(self):
        if self.use_pg:
            return self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self._conn.cursor()

    @staticmethod
    def _adapt_sql(sql: str) -> str:
        # psycopg2 用 %s；保留 ? 給 SQLite。注意：DDL 內若有真的 ? 不會出現（我們不寫）
        return sql.replace("?", "%s") if USE_POSTGRES else sql

    def execute(self, sql: str, params: Sequence[Any] = ()):
        cur = self._cursor()
        cur.execute(self._adapt_sql(sql), tuple(params))
        return cur

    def executemany(self, sql: str, seq_params: Iterable[Sequence[Any]]):
        cur = self._cursor()
        cur.executemany(self._adapt_sql(sql), [tuple(p) for p in seq_params])
        return cur

    def commit(self) -> None:
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


def get_db() -> DBConnection:
    return DBConnection()


# --------- 方言相依的 DDL ---------
_DDL_SQLITE = [
    """CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at    TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )""",
    """CREATE TABLE IF NOT EXISTS projects (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        description TEXT NOT NULL,
        tech_stack  TEXT NOT NULL,
        image_url   TEXT,
        demo_url    TEXT,
        github_url  TEXT,
        created_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )""",
    """CREATE TABLE IF NOT EXISTS messages (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        email      TEXT NOT NULL,
        content    TEXT NOT NULL,
        is_read    INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )""",
    """CREATE TABLE IF NOT EXISTS profile (
        id         INTEGER PRIMARY KEY,
        name       TEXT NOT NULL,
        title      TEXT NOT NULL,
        bio        TEXT NOT NULL,
        avatar_url TEXT,
        email      TEXT,
        github     TEXT,
        linkedin   TEXT,
        updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    )""",
]

_DDL_POSTGRES = [
    """CREATE TABLE IF NOT EXISTS users (
        id            SERIAL PRIMARY KEY,
        username      TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )""",
    """CREATE TABLE IF NOT EXISTS projects (
        id          SERIAL PRIMARY KEY,
        title       TEXT NOT NULL,
        description TEXT NOT NULL,
        tech_stack  TEXT NOT NULL,
        image_url   TEXT,
        demo_url    TEXT,
        github_url  TEXT,
        created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )""",
    """CREATE TABLE IF NOT EXISTS messages (
        id         SERIAL PRIMARY KEY,
        name       TEXT NOT NULL,
        email      TEXT NOT NULL,
        content    TEXT NOT NULL,
        is_read    BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )""",
    """CREATE TABLE IF NOT EXISTS profile (
        id         INTEGER PRIMARY KEY,
        name       TEXT NOT NULL,
        title      TEXT NOT NULL,
        bio        TEXT NOT NULL,
        avatar_url TEXT,
        email      TEXT,
        github     TEXT,
        linkedin   TEXT,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )""",
]


def init_db() -> None:
    """建立四張資料表（若不存在）— 自動依連線目標選用對應方言的 DDL。"""
    ddl = _DDL_POSTGRES if USE_POSTGRES else _DDL_SQLITE
    conn = get_db()
    try:
        for stmt in ddl:
            conn.execute(stmt)
        conn.commit()
    finally:
        conn.close()


def db_info() -> dict:
    """供啟動時 log 用，知道現在連到哪個資料庫。"""
    return {"engine": "postgresql" if USE_POSTGRES else "sqlite",
            "target": DATABASE_URL.split("@")[-1] if USE_POSTGRES else str(SQLITE_PATH)}


if __name__ == "__main__":
    init_db()
    print("[db] OK ->", db_info())
