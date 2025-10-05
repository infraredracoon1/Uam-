import sqlite3, datetime, json
from .database import DB_PATH

def add_constant(name, value, scale, derivation, explanation,
                 validated=True, validation_source="analytical"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO constants VALUES (?,?,?,?,?,?,?,?)
    """, (
        name, value, scale, derivation, explanation,
        validated, validation_source,
        datetime.datetime.utcnow().isoformat()
    ))
    conn.commit(); conn.close()

def add_equation(name, expression, variables, derivation,
                 explanation, is_verified=True):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO equations (name, expression, variables, derivation, explanation,
                           is_verified, timestamp)
    VALUES (?,?,?,?,?,?,?)
    """, (
        name, str(expression), json.dumps(variables),
        derivation, explanation, is_verified,
        datetime.datetime.utcnow().isoformat()
    ))
    conn.commit(); conn.close()

def log_failure(context, message, reason):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO failures (context, message, reason, timestamp)
    VALUES (?,?,?,?)
    """, (context, message, reason, datetime.datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
