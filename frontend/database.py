import sqlite3

def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (timestamp TEXT, diagnosis TEXT, confidence REAL)''')
    conn.commit()

def insert_report(timestamp, diagnosis, confidence):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("INSERT INTO reports VALUES (?, ?, ?)", (timestamp, diagnosis, confidence))
    conn.commit()

def fetch_history():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY timestamp DESC")
    return c.fetchall()
