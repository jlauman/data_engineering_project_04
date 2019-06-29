import os
import configparser
# import pandas as pd
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ShortType, DoubleType, DateType
from pyspark.sql import functions as F

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

spark = SparkSession \
    .builder \
    .master('yarn') \
    .appName("Sparkify AWS EMR ETL") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
    .getOrCreate()

spark.newSession()
print(spark)

input_path = "s3a://udacity-dend/log_data/*/*/*.json"
df = spark.read.json(input_path)
df.printSchema()

os.environ['AWS_ACCESS_KEY_ID'] = config['S3']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['S3']['AWS_SECRET_ACCESS_KEY']


df.write.csv('s3a://jlauman-project-04/log_data.csv')
