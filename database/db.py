import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               name TEXT,
               age INTEGER
               )
''')

cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Анна", 14))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Влад", 12))

conn.commit()