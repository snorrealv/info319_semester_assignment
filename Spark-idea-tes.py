import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType


# Create a SparkSession
findspark.init()
findspark.add_packages('org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0')

spark = SparkSession \
    .builder \
    .appName("Kafka Stream to Spark DataFrame") \
    .getOrCreate()

# Create a DataFrame from the Kafka stream
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
  .option("subscribe", "tweet_explicit") \
  .option("startingOffsets", "earliest") \
  .load() \
  .select(from_json(col("value").cast("string"), schema).alias("json_data")) \
  .select(col("json_data.*"))

# Select the columns we want to keep
df = df.select(col("key").cast("string"), col("value").cast("string"), col("timestamp"))

# Start the stream
query = df \
  .writeStream \
  .outputMode("append") \
  .format("console") \
  .start() \
  .awaitTermination()