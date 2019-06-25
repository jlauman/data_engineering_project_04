import os
import configparser
import pandas as pd
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
    .master('local[*]') \
    .appName("Sparkify AWS EMR ETL") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
    .getOrCreate()

spark.newSession()

# spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", config['S3']['AWS_ACCESS_KEY_ID'])
# spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", config['S3']['AWS_SECRET_ACCESS_KEY'])

# spark._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId", config['S3']['AWS_ACCESS_KEY_ID'])
# spark._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", config['S3']['AWS_SECRET_ACCESS_KEY'])

# # see https://github.com/databricks/spark-redshift/issues/298#issuecomment-271834485
# spark.sparkContext.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")

# # see https://stackoverflow.com/questions/28844631/how-to-set-hadoop-configuration-values-from-pyspark
# hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

# # # see https://stackoverflow.com/questions/43454117/how-do-you-use-s3a-with-spark-2-1-0-on-aws-us-east-2
# hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
# hadoop_conf.set("com.amazonaws.services.s3.enableV4", "true")
# hadoop_conf.set("fs.s3a.access.key", config['S3']['AWS_ACCESS_KEY_ID'])
# hadoop_conf.set("fs.s3a.secret.key", config['S3']['AWS_SECRET_ACCESS_KEY'])

# # # see http://blog.encomiabile.it/2015/10/29/apache-spark-amazon-s3-and-apache-mesos/
# # hadoop_conf.set("fs.s3a.connection.maximum", "100000")

# # see https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
# hadoop_conf.set("fs.s3a.endpoint", "s3." + 'us-east-2' + ".amazonaws.com")


print(spark)

# input_path = "s3a://jlauman-dend-project-04/log_data/*/*/*.json"
input_path = "s3a://udacity-dend/log_data/*/*/*.json"
df = spark.read.json(input_path)
df.printSchema()


os.environ['AWS_ACCESS_KEY_ID'] = config['S3']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['S3']['AWS_SECRET_ACCESS_KEY']


df.write.csv('s3a://jlauman-dend-project-04-bucket2/log_data.csv')
