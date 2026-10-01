import csv
import os
import psycopg

password = os.getenv("POSTGRES_PASSWORD")

INPUT_FILE = "../day-04/data/orders.csv"
CUSTOMERS_FILE = "../day-02/output/clean_customers.csv"
VALID_ORDERS_FILE = "output/valid_orders.csv"
REJECTED_ORDERS_FILE = "output/rejected_orders.csv"


def get_customer_ids():
    customer_ids = set()

    with open(CUSTOMERS_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customer_id = int(row["customer_id"])
            customer_ids.add(customer_id)

    return customer_ids


def validate_orders(customer_ids):
    valid_orders = []
    rejected_orders = []

    with open(INPUT_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                row["order_id"] = int(row["order_id"])
                row["customer_id"] = int(row["customer_id"])
                row["amount"] = int(row["amount"])
                row["quantity"] = int(row["quantity"])

            except ValueError:
                row["reason"] = "invalid_amount"
                rejected_orders.append(row)
                continue

            if row["quantity"] <= 0:
                row["reason"] = "invalid_quantity"
                rejected_orders.append(row)
                continue

            if row["amount"] <= 0:
                row["reason"] = "invalid_amount"
                rejected_orders.append(row)
                continue

            if row["customer_id"] not in customer_ids:
                row["reason"] = "customer_not_found"
                rejected_orders.append(row)
                continue

            valid_orders.append(row)

    return valid_orders, rejected_orders


def write_valid_orders(valid_orders):
    with open(VALID_ORDERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id",
                "customer_id",
                "product",
                "quantity",
                "amount",
            ],
        )

        writer.writeheader()
        writer.writerows(valid_orders)


def write_rejected_orders(rejected_orders):
    with open(REJECTED_ORDERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id",
                "customer_id",
                "product",
                "quantity",
                "amount",
                "reason",
            ],
        )

        writer.writeheader()
        writer.writerows(rejected_orders)


def load_orders_to_postgres(conn, valid_orders):
    for row in valid_orders:
        conn.execute(
            """
            INSERT INTO daily_orders
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (order_id)
            DO UPDATE SET
                customer_id = EXCLUDED.customer_id,
                product = EXCLUDED.product,
                quantity = EXCLUDED.quantity,
                amount = EXCLUDED.amount
            """,
            (
                row["order_id"],
                row["customer_id"],
                row["product"],
                row["quantity"],
                row["amount"],
            ),
        )

    conn.commit()


def verify_load(conn, valid_orders):
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM daily_orders;
    """)

    loaded_orders = cur.fetchone()[0]

    print("Valid orders:", len(valid_orders))
    print("Loaded orders:", loaded_orders)

    if loaded_orders == len(valid_orders):
        print("✅ Data load verification passed")
    else:
        print("❌ Data load verification failed")


def main():
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="de_learning",
        user="postgres",
        password=password,
    )

    print("🎉 Connected to PostgreSQL successfully!")

    customer_ids = get_customer_ids()

    valid_orders, rejected_orders = validate_orders(customer_ids)

    total_orders = len(valid_orders) + len(rejected_orders)
    print("Total orders:", total_orders)

    write_valid_orders(valid_orders)
    write_rejected_orders(rejected_orders)

    load_orders_to_postgres(conn, valid_orders)

    verify_load(conn, valid_orders)

    conn.close()


if __name__ == "__main__":
    main()
