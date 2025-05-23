def create_tables():
    conn = sqlite3.connect("products.db")
    conn.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        priceWas REAL,
        priceIs REAL,
        difference REAL,
        discount REAL,
        link TEXT UNIQUE,
        image TEXT
    )''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id TEXT PRIMARY KEY
    )''')
    conn.commit()
    conn.close()
