import sqlite3

DB_NAME = "users.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    pocket_id TEXT,
                    approved INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

# Check if user exists
def user_exists(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

# Save new user
def save_user(user_id, pocket_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, pocket_id, approved) VALUES (?, ?, 0)",
              (user_id, pocket_id))
    conn.commit()
    conn.close()

# Approve user
def approve_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET approved=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

# Get approved users
def get_approved_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE approved=1")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# Initialize on first run
init_db()
