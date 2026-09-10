import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, status TEXT)")
conn.commit()

def set_status(user_id, status):
    cursor.execute("REPLACE INTO users (user_id, status) VALUES (?, ?)", (user_id, status))
    conn.commit()

def get_status(user_id):
    cursor.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return "Неизвестно"


    