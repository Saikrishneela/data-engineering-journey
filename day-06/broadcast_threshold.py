import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
python_executable = project_root / ".venv-spark" / "Scripts" / "python.exe"
os.environ["PYSPARK_PYTHON"] = str(python_executable)
os.environ["PYSPARK_DRIVER_PYTHON"] = str(python_executable)

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ThresholdTest").master("local[*]").getOrCreate()

orders = spark.read.csv("../day-04/data/orders.csv", header=True, inferSchema=True)
customers = spark.read.csv(
    "../day-02/data/customers.csv", header=True, inferSchema=True
)

spark.conf.set("spark.sql.adaptive.enabled", "false")

print("=========== DEFAULT THRESHOLD (10 MB), NO HINT =======")
orders.join(customers, "customer_id").explain()

spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

print("======== THRESHOLD = -1, NO HINT ======")
orders.join(customers, "customer_id").explain()
