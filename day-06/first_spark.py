import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
python_executable = project_root / ".venv-spark" / "Scripts" / "python.exe"

os.environ["PYSPARK_PYTHON"] = str(python_executable)
os.environ["PYSPARK_DRIVER_PYTHON"] = str(python_executable)

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, when, col
from pyspark.sql import functions as f

spark = (
    SparkSession.builder.appName("FirstSparkProgram").master("local[*]").getOrCreate()
)

data = [
    (101, "Ravi", 500),
    (102, "Priya", 300),
    (103, "Arun", 700),
]

columns = ["order_id", "customer_name", "amount"]

orders = spark.createDataFrame(data, columns)

# orders.show()

high_value_orders = orders.filter(orders.amount > 400)
# high_value_orders.show()


data = [
    (1, "sai", 500),
    (2, "rahul", 450),
    (3, "sanjay", 520),
    (4, "manish", 560),
]

columns = ["id", "name", "amount"]

friends = spark.createDataFrame(data, columns)
# friends.show()

highID = (
    friends.filter(friends.id > 2)
    .withColumn("tax_amount", friends.amount * 0.10)
    .select("*")
)
# highID.show()


rows = [
    ("ronaldo", 500),
    ("bale", 450),
    ("kroos", 300),
    ("ramos", 480),
    ("ronaldo", 600),
    (None, 480),
    ("messi", None),
    ("kroos", 550),
]

columns = ["players", "goals"]

footBallData = spark.createDataFrame(rows, columns)

# footBallData.show()
# footBallData.dropna().show()

# footBallData.fillna({"players": "mercelo", "goals": 0}).show()


result = footBallData.groupBy(footBallData.players).agg(
    sum(footBallData.goals).alias("total_goals"),
    count("*").alias("goals_records"),
)
# result.filter(result.total_goals > 800).orderBy("total_goals", ascending=False).show()

classified_players = footBallData.withColumn(
    "player_level",
    when((footBallData.goals.isNull()) | (footBallData.players.isNull()), "UNKNOWN")
    .when(footBallData.goals >= 600, "LEGEND")
    .when((footBallData.goals >= 500) & (footBallData.goals <= 599), "ELITE")
    .otherwise("BEST"),
)

# classified_players.show()


rows = [
    (101, "Laptop", 75000, 2),
    (102, "Phone", 30000, 1),
    (103, "Headphones", 2000, 5),  # each rows in dataFrame
    (104, "Laptop", 75000, 1),
    (105, "Phone", None, 2),
    (106, None, 1500, 3),
    (107, "Keyboard", 3000, 4),
    (108, "Monitor", 12000, 2),
]

columns = [
    "order_id",
    "product",
    "price",
    "quantity",
]  ##  each column name in Dataframe

orders_df = spark.createDataFrame(
    rows, columns
)  # spark.createDataFrame(rows, columns) creates a Spark DataFrame using the supplied rows and column names, then assigns it to orders_df.
# orders_df.show()  # displaying dataFrame name is orders_df


def summarized_products(orders_df, premium_threshold, mid_threshold):
    cleaned_data_product = (
        orders_df.dropna(
            subset=["product", "price", "quantity"]
        )  ##  It removes rows with missing values in any column by default. In your dataset, rows 105 and 106 are removed because product ad quantity are null.
        .withColumn(
            "revenue", col("price") * col("quantity")
        )  ## adds a new column quantity * prize gives total reveune
        .groupBy("product")  ## group the similar product-items
        .agg(
            sum("revenue").alias(
                "total_revenue"
            ),  ## sum(orders_df.price) → sum of prices.
            sum("quantity").alias(
                "total_quantity"
            ),  ## sum(orders_df.quantitiy) → sum of quantities.
        )
        .withColumn(
            "price_category",  ## creates a new column name price_category and give them a category based on pricevalue
            when(col("total_revenue") >= premium_threshold, "premium")
            .when(col("total_revenue") >= mid_threshold, "mid-range")
            .otherwise("regular_price"),
        )
        .orderBy(
            "total_revenue", ascending=False
        )  ## sorts the resultiog based on total_price from high to low
    )

    return cleaned_data_product


# call the function

product_summary = summarized_products(orders_df, 60000, 15000)
# product_summary.show()  ## displaying the cleaned DataFrame


print("===================== NEW DataFrame ======================")


# Create 500 products
product_rows = [
    (
        product_id,
        f"Product_{product_id}",
        ["Electronics", "Furniture", "Accessories", "Home"][product_id % 4],
    )
    for product_id in range(1, 501)
]

product_columns = ["product_id", "product_name", "category"]

products_df = spark.createDataFrame(product_rows, product_columns)


# Create 10,000 orders
order_rows = [
    (
        order_id,
        (order_id % 520) + 1,
        (order_id % 10) + 1,
    )
    for order_id in range(1, 10001)
]

order_columns = ["order_id", "product_id", "quantity"]

orders_large_df = spark.createDataFrame(order_rows, order_columns)

# orders_large_df.show(5)
# products_df.show(5)

## ============================== JOINS =============================== ##

inner_joined_df = orders_large_df.join(products_df, on="product_id", how="inner")
# inner_joined_df.show(5)


left_joined_df = orders_large_df.join(products_df, on="product_id", how="left")
# left_joined_df.show(5)

left_anti_joined_df = products_df.join(
    orders_large_df, on="product_id", how="left_anti"
)
# left_anti_joined_df.show(5)

full_joined_df = products_df.join(orders_large_df, on="product_id", how="full")
# full_joined_df.show(10)

missing_products_df = orders_large_df.join(
    products_df, on="product_id", how="left_anti"
)
# missing_products_df.show(5)

Unmatching_orders = orders_large_df.join(
    products_df, on="product_id", how="left_anti"
).select("order_id", "product_id")

# Unmatching_orders.show()

# print(Unmatching_orders.count())


missing_product_name = orders_large_df.join(
    products_df, on="product_id", how="left"
).filter(col("product_name").isNull())
# missing_product_name.show()
# print(missing_product_name.count())

missing_products = products_df.join(orders_large_df, on="product_id", how="left_anti")
# missing_products.show()
# print(missing_products.count())

broadcast_shuffle_df = orders_large_df.join(
    f.broadcast(products_df), on="product_id", how="inner"
)

inner_joined_df.explain("formatted")

broadcast_shuffle_df.explain("formatted")

print(spark.conf.get("spark.sql.autoBroadcastJoinThreshold"))
print(spark.conf.get("spark.sql.adaptive.enabled"))


spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.adaptive.enabled", "false")

inner_joined_df.explain("formatted")

broadcast_shuffle_df.explain("formatted")

print(spark.conf.get("spark.sql.autoBroadcastJoinThreshold"))

print(spark.conf.get("spark.sql.adaptive.enabled"))
