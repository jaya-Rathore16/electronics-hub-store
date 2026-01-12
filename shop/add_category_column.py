import sqlite3

conn = sqlite3.connect("products.db")
cur = conn.cursor()

cur.execute("ALTER TABLE products ADD COLUMN category TEXT")

conn.commit()
conn.close()

print("Category column added!")
