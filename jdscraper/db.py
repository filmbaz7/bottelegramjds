import sqlite3

def get_connection():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            priceWas REAL,
            priceIs REAL,
            difference REAL,
            discount REAL,
            link TEXT UNIQUE,
            image TEXT
        )
    ''')
    conn.commit()
    return conn
