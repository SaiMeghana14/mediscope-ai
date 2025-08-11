import sqlite3
from datetime import datetime
import bcrypt

DB_NAME = "mediscope.db"

# -------------------------------
# Create main tables if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            feedback TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            role TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

# -------------------------------
# Save new user (with hashed password)
def save_user(username, password, email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
    ''', (username, hashed_pw, email))

    conn.commit()
    conn.close()

# -------------------------------
# Verify user login
def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_pw = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_pw)
    return False

# -------------------------------
# Save feedback to DB
def save_feedback(name, email, feedback):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO feedback (name, email, feedback)
        VALUES (?, ?, ?)
    ''', (name, email, feedback))

    conn.commit()
    conn.close()

# -------------------------------
# Save chat messages
def save_chat(user, message, role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO chat_history (user, message, role)
        VALUES (?, ?, ?)
    ''', (user, message, role))

    conn.commit()
    conn.close()

# -------------------------------
# Retrieve all feedback entries
def get_all_feedback():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, feedback, timestamp FROM feedback ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------------
# Retrieve all chat history
def get_all_chat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user, message, role, timestamp FROM chat_history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
