import sqlite3

db = sqlite3.connect("slh_core.db")

cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS investors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT,
    full_name TEXT,
    phone TEXT,
    email TEXT,
    investment_amount REAL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS project_events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    event_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS decisions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

db.commit()

print("SLH CORE DB READY")


