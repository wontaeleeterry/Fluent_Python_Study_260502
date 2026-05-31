import sqlite3


class CustomerRepository:

    def save(self, customer):

        conn = sqlite3.connect("shop.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO customers(
                name,
                email
            )
            VALUES (?, ?)
            """,
            (
                customer.name,
                customer.email.value
            )
        )

        customer_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return customer_id