"""
Database initialization and connection helpers.
Uses SQLite for simplicity — easily swap for PostgreSQL/MySQL later.
"""

import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DB_PATH", "../voicebot.db")


def get_db_connection():
    """Return a SQLite connection with row_factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id      TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            order_details TEXT NOT NULL,
            service_type  TEXT NOT NULL DEFAULT 'all',  -- medical / restaurant / business / all
            language      TEXT NOT NULL DEFAULT 'en',   -- en / hi / kn / mr / te
            status        TEXT NOT NULL DEFAULT 'pending',
            call_sid      TEXT,
            speech_result TEXT,
            intent        TEXT,
            notes         TEXT,
            retry_count   INTEGER DEFAULT 0,
            created_at    TEXT,
            updated_at    TEXT
        )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")
