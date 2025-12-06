import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
               id INTEGER PRIMARY KEY,
               food_type TEXT,
               name_client TEXT,
               adress TEXT,
               phone_number TEXT
               )
''')

cursor.execute("INSERT INTO orders (food_type, name_client, adress, phone_number) VALUES (?, ?, ?, ?)", ("Вкусная", "Вася Пупкин", "Улица Пушкина 66666", "+4444"))
cursor.execute("INSERT INTO orders (food_type, name_client, adress, phone_number) VALUES (?, ?, ?, ?)", ("Невкусная", "Андрей", "Улица Ленина 66666", "+666"))
cursor.execute("INSERT INTO orders (food_type, name_client, adress, phone_number) VALUES (?, ?, ?, ?)", ("Вся еда", "Николай", "Улица Сталина 66666", "+6767"))

conn.commit()