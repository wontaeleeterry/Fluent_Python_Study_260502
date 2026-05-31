import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# 고객 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# 주문 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    total_amount INTEGER NOT NULL,
    FOREIGN KEY(customer_id)
        REFERENCES customers(id)
)
""")

conn.commit()
conn.close()