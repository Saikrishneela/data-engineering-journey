import csv
import os

import psycopg

INPUT_FILE = "../day-02/data/customers.csv"

password = os.getenv("POSTGRES_PASSWORD")
if not password:
    raise SystemExit("Set the POSTGRES_PASSWORD environment variable first.")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="de_learning",
    user="postgres",
    password=password,
) as conn:
    print("🎉 connected to PostgreSQL successfully!")

    with conn.cursor() as cur:
        with open(INPUT_FILE, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"].strip()
                email = row["email"].strip()
                city = row["city"].strip()

                if name == "" or email == "" or city == "" or "@" not in email:
                    continue

                try:
                    customer_id = int(row["customer_id"])
                    age = int(row["age"])
                except ValueError:
                    print("Invalid data:", row)
                    continue

                cur.execute(
                    """
                    INSERT INTO customers (customer_id, name, email, city, age)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (customer_id)
                    DO UPDATE SET
                        name  = EXCLUDED.name,
                        email = EXCLUDED.email,
                        city  = EXCLUDED.city,
                        age   = EXCLUDED.age
                    """,
                    (customer_id, name, email, city, age),
                )

        conn.commit()

        cur.execute("SELECT * FROM customers ORDER BY customer_id LIMIT 10")
        for row in cur.fetchall():
            print(row)
