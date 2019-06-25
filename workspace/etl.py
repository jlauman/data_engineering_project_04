import os
import configparser
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ShortType, DoubleType, DateType
from pyspark.sql import functions as F


config = configparser.ConfigParser()
config.read('dl.cfg')

# credentails for input (udacity-dend) bucket must be empty
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def read_song_data(spark, input_data_path):
    print('\nread_song_data...')

    # get filepath to song data file
    song_data_path = input_data_path + 'song_data/A/A/A/*.json'

    song_schema = StructType([
        StructField("artist_id", StringType(), True),
        StructField("artist_name", StringType(), True),
        StructField("artist_location", StringType(), True),
        StructField("artist_latitude", DoubleType(), True),
        StructField("artist_longitude", DoubleType(), True),
        StructField("song_id", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("title", StringType(), True),
        StructField("year", ShortType(), True),
    ])

    # read song data files
    song_df = spark.read.json(song_data_path, song_schema)
    song_df.printSchema()

    # extract columns to create artists dimension table
    d_artist_df = song_df.select('artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude') \
        .dropDuplicates(['artist_id'])
    print('artist dimension record count:', d_artist_df.count())

    # extract columns to create songs dimension table
    d_song_df = song_df.select('song_id', 'title', 'artist_id', 'year', 'duration')
    print('song dimension record count:', d_song_df.count())

    return d_artist_df, d_song_df


def read_log_data(spark, input_data_path):
    print('\nread_log_data...')

    # get filepath to log data file
    log_data_path = input_data_path + 'log_data/*/*/*.json'

    # read log data (event) data files
    # and filter by actions for song plays
    # and create parsed timestamp column and formatted start_time column
    event_df = spark.read.json(log_data_path) \
        .filter(F.col('page') == 'NextSong') \
        .withColumn('timestamp', F.from_unixtime(F.col('ts') / 1000)) \
        .withColumn('start_time', F.date_format('timestamp', 'yyyyMMddHH'))
    event_df.printSchema()

    # extract columns for user dimension table    
    d_user_df = event_df.select('userId', 'lastName', 'firstName', 'gender') \
        .dropDuplicates(['userId'])
    print('user dimension record count: ', d_user_df.count())

    # extract columns to create time dimension table
    d_time_df = event_df.select('timestamp', 'start_time') \
        .withColumn('year', F.year('timestamp')) \
        .withColumn('month', F.month('timestamp')) \
        .withColumn('day', F.dayofmonth('timestamp')) \
        .withColumn('hour', F.hour('timestamp')) \
        .withColumn('week_of_year', F.weekofyear('timestamp')) \
        .withColumn('weekday', F.dayofweek('timestamp')) \
        .select(['start_time', 'year', 'month', 'day', 'hour', 'week_of_year', 'weekday']) \
        .dropDuplicates(['start_time'])
    print('time dimension record count:', d_time_df.count())

    return event_df, d_user_df, d_time_df


def make_songplay_data(d_artist_df, d_song_df, event_df):
    print('\nmake_songplay_data...')

    tmp_df = d_song_df.withColumnRenamed('artist_id', 'song_artist_id')
    tmp_df = tmp_df.join(d_artist_df, d_artist_df.artist_id == tmp_df.song_artist_id) \
        .select('song_id', 'title', 'duration', 'artist_id', 'artist_name')

    comparison = [event_df.song == tmp_df.title, event_df.length.cast(ShortType()) == tmp_df.duration.cast(ShortType())]

    # extract columns from joined song and log datasets to create songplays table 
    f_songplay_df = event_df.withColumn('songplay_id', F.sha1(F.concat_ws('|', 'timestamp', 'userId', 'song'))) \
        .join(tmp_df, comparison, 'left') \
        .select(['songplay_id', 'start_time', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent'])
    print('songplay fact record count:', f_songplay_df.count())

    not_null_count = f_songplay_df.filter(F.col('song_id').isNotNull()).count()
    print('songplay fact records with song_id value:', not_null_count)

    return f_songplay_df


def write_d_song_df(spark, d_song_df, output_data_path):
    path = output_data_path + 'd_song_df.parquet'
    print('\nwrite_d_song_df to ' + path)
    # write songs table to parquet files partitioned by year and artist
    d_song_df.write.parquet(path, mode='overwrite')
    # d_song_df.write.csv(path)


def write_d_artist_df(spark, d_artist_df):
    # write artists table to parquet files
    # artists_table
    pass


def write_d_user_df(spark, d_user_df):
    pass
    # write users table to parquet files
    # artists_table

def write_d_time_df(spark, d_time_df):
    # write time table to parquet files partitioned by year and month
    # time_table
    pass

def write_f_songplay_df(spark, f_songplay_df):
    # write songplays table to parquet files partitioned by year and month
    # songplays_table
    pass


def main():
    spark = create_spark_session()
    input_data_path = "s3a://udacity-dend/"
    # use bucket in us-east (N. Virginia); this doesn't work with us-east-2 region
    output_data_path = "s3a://jlauman-dend-project-04-bucket2/output/"
    
    d_artist_df, d_song_df = read_song_data(spark, input_data_path)

    # event_df, d_user_df, d_time_df = read_log_data(spark, input_data_path)

    # f_songplay_df = make_songplay_data(d_artist_df, d_song_df, event_df)

    # set credentials for S3 output bucket
    os.environ['AWS_ACCESS_KEY_ID'] = config['S3']['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['S3']['AWS_SECRET_ACCESS_KEY']

    write_d_song_df(spark, d_song_df, output_data_path)



if __name__ == "__main__":
    main()
