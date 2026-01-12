import sqlite3

conn = sqlite3.connect("products.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER,
    image TEXT
)
""")

conn.commit()
conn.close()

print("Database created!")
