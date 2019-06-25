import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ShortType, DoubleType, DateType
from pyspark.sql import functions as F

spark = SparkSession \
    .builder \
    .master('local[*]') \
    .appName("Sparkify AWS EMR ETL") \
    .getOrCreate()

spark.newSession()

print(spark)
