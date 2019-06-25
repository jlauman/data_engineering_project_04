# Project 4: Data Lake


## AWS Configuration

region: us-east-2


aws s3 sync data/log_data/ s3://jlauman-dend-project-04/log_data

aws s3 sync data/song_data/ s3://jlauman-dend-project-04/song_data


jupyter lab --notebook-dir=workspace/

Must add inbound SSH to EMR master node ec2 security group.

/usr/lib/spark/bin/pyspark
sc._conf.getAll()

sudo lsof -i -P -n | grep LISTEN

sc.uiWebUrl
spark.sparkContext._conf.getAll()

for item in sorted(sc._conf.getAll()): print(item)


sudo pip install git pandas pyspark configparser


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




bin/build_spark_image.sh
bin/build_jupyter_image.sh
bin/run_spark_stack.sh

## PySpark Reference

https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PySpark_Cheat_Sheet_Python.pdf
https://www.qubole.com/resources/pyspark-cheatsheet/
http://mail-archives.apache.org/mod_mbox/spark-user/201612.mbox/%3CCAFbeQtEuiioyjVy7PXfn9cXk_=ybq6hAK5ToHcmf85wPwmTbJA@mail.gmail.com%3E

https://stackoverflow.com/questions/52292180/pyspark-generate-row-hash-of-specific-columns-and-add-it-as-a-new-column

### Set Up Key Pair for Master/Worker

ssh-keygen -t rsa -P '' -f ./id_rsa

### Set Up Anaconda

The Anaconda package manager is used in this solution.
Follow the installation instruction at <https://docs.anaconda.com/anaconda/install/>.
After the `conda` command is available the shell run the following.

    conda create --name dend_project_04 python=2.7
    conda activate dend_project_04
    conda install jupyterlab pandas
    conda install pyspark
    pip install ipython-sql

Also, set the Jupyter notebook password.

    jupyter notebook password

Use the `bin/run_jupyter.sh` script to start and verify the Jupyter environment functions.


### Local Download of S3 Bucket Data

The local PostgreSQL prototype uses local data files. Install the AWS command line interface (cli)
tool for the local operating system.

On a Mac OS X/macOS box with homebrew installed do the following:

    brew install awscli

The URL for the S3 bucket data is: https://udacity-dend.s3.amazonaws.com/

Run the following command to download the S3 bucket data.

    aws s3 sync s3://udacity-dend/song_data ./data/song_data --no-sign-request
    aws s3 sync s3://udacity-dend/log_data ./data/log_data --no-sign-request
    aws s3 sync s3://udacity-dend/log_json_path.json ./data/log_json_path.json --no-sign-request



### Run Jupyter Labs

    bin/run_jupyter.sh


## Extra: Copy Project's Jupyter Workspace

    zip -r workspace.zip workspace
    mv workspace.zip workspace_original.zip
    mv workspace_original.zip workspace
