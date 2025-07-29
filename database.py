import sqlite3

# Connect to database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    pocket_id TEXT,
    approved INTEGER DEFAULT 0,
    strategy TEXT,
    timeframe TEXT
)
""")
conn.commit()

def add_user(user_id, pocket_id):
    cursor.execute("INSERT INTO users (id, pocket_id) VALUES (?, ?)", (user_id, pocket_id))
    conn.commit()

def user_exists(user_id):
    cursor.execute("SELECT id FROM users WHERE id=?", (user_id,))
    return cursor.fetchone() is not None

def approve_user(user_id):
    cursor.execute("UPDATE users SET approved=1 WHERE id=?", (user_id,))
    conn.commit()

def is_approved(user_id):
    cursor.execute("SELECT approved FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1

def set_strategy(user_id, strategy):
    cursor.execute("UPDATE users SET strategy=? WHERE id=?", (strategy, user_id))
    conn.commit()

def set_timeframe(user_id, tf):
    cursor.execute("UPDATE users SET timeframe=? WHERE id=?", (tf, user_id))
    conn.commit()

def get_approved_users():
    cursor.execute("SELECT id, strategy, timeframe FROM users WHERE approved=1")
    return cursor.fetchall()
