
customers = {
    1: {
        "customer_id": 1,
        "name": "Ravi",
        "plan": "BasicPlan"
    },
    2: {
        "customer_id": 2,
        "name": "Priya",
        "plan": "ProPlan"
    },
    3: {
        "customer_id": 3,
        "name": "John",
        "plan": "EnterprisePlan"
    }
}


def get_customer(customer_id):
    return customers.get(
        customer_id,
        {"error": "Customer not found"}
    )
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "orders.db"


def setup_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            status TEXT
        )
    """)

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, status)
        VALUES (?, ?, ?)
    """, [
        (1042, 2, "Shipped"),
        (1043, 1, "Processing"),
        (1044, 3, "Delivered")
    ])

    connection.commit()
    connection.close()


def get_order_status(order_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT order_id, customer_id, status FROM orders WHERE order_id = ?",
        (order_id,)
    )

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return {"error": "Order not found"}

    return {
        "order_id": result[0],
        "customer_id": result[1],
        "status": result[2]
    }


if __name__ == "__main__":
    setup_database()
    print("Order database created successfully!")