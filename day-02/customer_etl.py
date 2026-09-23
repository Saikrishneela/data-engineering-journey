import csv

input_file = "data/customers.csv"
clean_output = "output/clean_customers.csv"  # Reading the files
invalid_output = "output/invalid_customers.csv"

seen_customer_ids = (
    set()
)  # creating a set so that we can eliminate if we found any duplicate


def clean_customer(row):
    name = row["name"].strip()
    city = row["city"].strip()
    email = row["email"].strip().lower()

    try:
        age = int(row["age"])
    except ValueError:
        return None

    return name, city, email, age


def validate_customer(row, name, city, email):
    customer_id = row["customer_id"].strip()

    if customer_id == "":
        # print("Invalid customer: missing customer_id")
        return False

    if customer_id in seen_customer_ids:
        # print("Invalid customer: duplicate customer_id")
        return False

    if name == "":
        # print("Invalid customer: missing name")
        return False

    if city == "":
        # print("Invalid customer: missing city")
        return False

    if email == "":
        # print("Invalid customer: missing email")
        return False

    if "@" not in email:
        # print("Invalid customer: invalid email")
        return False

    seen_customer_ids.add(customer_id)

    return True


clean_customers = []
invalid_customers = []

with open(input_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        result = clean_customer(row)

        if result is None:
            # print("Invalid customer: invalid age")
            invalid_customers.append(row)
            continue

        name, city, email, age = result

        if not validate_customer(row, name, city, email):
            invalid_customers.append(row)
            continue

        clean_customers.append(
            {
                "customer_id": row["customer_id"].strip(),
                "name": name,
                "email": email,
                "city": city,
                "age": age,
            }
        )

with open(clean_output, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["customer_id", "name", "email", "city", "age"],
    )

    writer.writeheader()
    writer.writerows(clean_customers)


with open(invalid_output, "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["customer_id", "name", "email", "city", "age"],
    )

    writer.writeheader()
    writer.writerows(invalid_customers)
