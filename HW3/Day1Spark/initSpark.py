from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

spark = (
    SparkSession.builder.appName("SparkPySparkTutorial")
    .config("spark.ui.port", "4050")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

print("Spark version:", spark.version)

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]

df = spark.createDataFrame(data, columns)
df.show()

df_csv = spark.read.csv(
    "../Q1/yellow_tripdata_2019-01_short.csv", header=True, inferSchema=True
)
df_csv.show(5)


df_filtered = df_csv.select("VendorID", "trip_distance", "DOLocationID").filter(
    col("passenger_count") > 3
)

df_transformed = df_filtered
df_transformed.show()

grouped_df = df_csv.groupBy("DOLocationID").count()

# Show the results
grouped_df.show()
