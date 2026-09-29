import psycopg

import csv

inputfile = "../day-02/data/customers.csv"

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="de_learning",
    user="postgres",
    password="Saikrishna@30",
)

cur = conn.cursor()


print("🎉 connect to PostgreSQL successfully!")

with open(inputfile, "r") as file:
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
            """ INSERT INTO customers
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT(customer_id)
                DO UPDATE SET
                name  = EXCLUDED.name,
                email = EXCLUDED.email,
                city  = EXCLUDED.city,
                age   = EXCLUDED.age
              """,
            (customer_id, name, email, city, age),
        )
conn.commit()

cur.execute(""" 
    select *
    from customers
    order by customer_id
    limit 10
    """)


rows = cur.fetchall()

for row in rows:
    print(row)

# cur.execute(
# """
# INSERT INTO customers
# VALUES (%s, %s, %s, %s, %s)""",
# (200002, "Test Python", "python@test.com", "Hyderabad", 30),
# )

# conn.commit()


# db_row = cur.fetchone()

# print(db_row)
