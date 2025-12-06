import sqlite3

conn_f = sqlite3.connect("food.db")
cursor_f = conn_f.cursor()

cursor_f.execute(
    '''
    CREATE TABLE IF NOT EXISTS food(
        name TEXT,
        price INT,

    )

    INSERT INTO food(name, price) VALUES('Пицца маргарита', 10)
    INSERT INTO food(name, price) VALUES('Пицца сырная', 15)
    INSERT INTO food(name, price) VALUES('Пицца с мясом', 20)
    '''
)

conn_f.commit()
conn_f.close()