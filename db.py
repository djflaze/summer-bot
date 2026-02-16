import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?)", (user_id,))
    conn.commit()

def get_users():
    cursor.execute("SELECT user_id FROM users")
    return [u[0] for u in cursor.fetchall()]

def get_meta(key):
    cursor.execute("SELECT value FROM meta WHERE key=?", (key,))
    r = cursor.fetchone()
    return r[0] if r else None

def set_meta(key, value):
    cursor.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, value))
    conn.commit()