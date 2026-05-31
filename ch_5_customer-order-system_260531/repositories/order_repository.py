import sqlite3


class OrderRepository:

    def save(self, order):

        conn = sqlite3.connect("shop.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO orders(
                customer_id,
                product_name,
                total_amount
            )
            VALUES (?, ?, ?)
            """,
            (
                order.customer_id,
                order.product_name,
                order.total_amount.amount
            )
        )

        conn.commit()
        conn.close()

    def find_all(self):

        conn = sqlite3.connect("shop.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                o.id,
                c.name,
                o.product_name,
                o.total_amount
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.id
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows