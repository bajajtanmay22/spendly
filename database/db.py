import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count > 0:
        conn.close()
        return

    conn.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
    )
    user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

    expenses = [
        (user_id, 12.50,  'Food',          '2026-06-02', 'Groceries'),
        (user_id, 45.00,  'Bills',         '2026-06-05', 'Electricity bill'),
        (user_id, 8.75,   'Transport',     '2026-06-08', 'Bus pass top-up'),
        (user_id, 60.00,  'Health',        '2026-06-10', 'Pharmacy'),
        (user_id, 25.00,  'Entertainment', '2026-06-14', 'Cinema tickets'),
        (user_id, 89.99,  'Shopping',      '2026-06-18', 'Clothing'),
        (user_id, 15.00,  'Other',         '2026-06-22', 'Miscellaneous'),
        (user_id, 22.30,  'Food',          '2026-06-27', 'Restaurant dinner'),
    ]
    conn.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses
    )
    conn.commit()
    conn.close()
