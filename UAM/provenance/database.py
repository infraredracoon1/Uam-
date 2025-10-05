import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/UAM_provenance.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS constants(
        name TEXT PRIMARY KEY,
        value REAL,
        scale TEXT,
        derivation TEXT,
        explanation TEXT,
        validated BOOLEAN,
        validation_source TEXT,
        timestamp TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS equations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        expression TEXT,
        variables TEXT,
        derivation TEXT,
        explanation TEXT,
        is_verified BOOLEAN,
        timestamp TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS failures(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        context TEXT,
        message TEXT,
        reason TEXT,
        timestamp TEXT
    )
    """)
    conn.commit(); conn.close()

init_db()
