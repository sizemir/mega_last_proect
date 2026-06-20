import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ratings
                 (user_id TEXT, rating INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

def save_rating(user_id, rating):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO ratings (user_id, rating, date) VALUES (?, ?, ?)", (user_id, rating, now))
    conn.commit()
    conn.close()

def get_ratings(user_id):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT rating FROM ratings WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows