# Project 4: Data Lake

The music streaming company Sparkify has grown and wants to analyze their growing history of customer
event logs in the cloud. The current customer event logs are currently stored in an AWS S3 bucket.

The ETL pipeline for this project will use a Spark cluster created using AWS EMR.

The output of the `workspace/etl.py` PySpark script executed on the Spark cluster stored in the following bucket:

https://s3.console.aws.amazon.com/s3/buckets/jlauman-project-04

As part of the initial analysis step for this project a local Spark cluster was created using docker.
The discussion of the local cluster set up using docker is beyond the scope of this document.


## Lessons Learned

Run the Spark ETL process on a slice of the full data set to ensure that all the pieces (Python, Spark,
S3, EMR with EC2 instances) are working correctly.

Do not use region `us-east-2` for S3 buckets. Attempting to write to an S3 bucket in this region will
fail with an uninformative "null" error.

Over allocate worker nodes for the Spark cluster. Better to create them and not need the extra horsepower
than choke processing with lack of CPU and RAM.

Ensure that a job run in spark uses the correct orchestrator. I can into a scenario where I mistakenly
installed PySpark separate from the one provided by EMR and wasted time running the ETL process only
on the master node.

Understand how the Spark writer works. Without repartitioning the dataframe the default is the most
inefficient option -- thousands of small files that choke S3. Initial experience with this problem
resulted in the Spark job stalling for over an hour and then failing.

Even after repartitioning a dataframe using `partitionBy` can cause problems. For example attempting to
partition and write the songs dataframe by `year` and `artist_id` still caused problems when writing into
the S3 output bucket.


## Configure AWS EMR Cluster and Tools

DO NOT use region `us-east-2` for S3 bucket. It does not behave the same as other regions.

See: https://mapr.com/support/s/article/S3-connection-issues-in-certain-AWS-Regions?language=en_US

1. Create an IAM user with S3 list/read/write roles

2. Create S3 bucket in US East (N. Virginia) - DO NOT USE US East (Ohio).

3. Create EMR cluster using advanced options
    - Select Hadoop, JupyterHub and Spark
    - Use 1 master and 2 core nodes (the default)
    - Configure S3 folder in project bucket for cluster logging
    - Select existing EC2 key pair - create one first if none exist
    - Ensure checkbox is selected for cluster visible to all IAM users in account

4. Configure EMR master node for SSH access
    - Jump to the security group of the master node and open inbound port 22
    - Copy the SSH command from the cluster summary page (with "-i" argument)
    - Ensure SSH command work to establish terminal connection to server
    - Create ~hadoop/.ssh/config file (see below) with github private key and "chmod 600 config"
    - Create private key file and paste contents of private key beginning with "-----BEGIN OPENSSH PRIVATE KEY-----"
    - Run command "chmod 600 github_aws_ec2_rsa" to change permissions

    Host github.com
      IdentityFile ~/.ssh/github_aws_ec2_rsa

5. Install software packages
    - Run command "sudo yum install git"
    - Run command "sudo pip install configparser"

6. Clone git repository using SSH
    - Change into ~hadoop directory
    - Run command "git clone git@github.com:jlauman/data_engineering_project_04.git"

7. Configure VS Code remote extension
    - Install VS Code "Remote Development" extension
    - Configure remote extension to use ssh_config file as shown below
    - Replace EMR master DNS name with current cluster master node

    Host data_engineering_project_04
    HostName ec2-18-191-148-16.us-east-2.compute.amazonaws.com
    User hadoop
    PreferredAuthentications publickey
    IdentityFile /Users/jlauman/Projects/data_engineering_project_04_secret/project_keypair.pem

8. Populate `dl.cfg` file with S3 credentials
    - Insert access key ID and secret from IAM user into `dl.cfg` file

    [S3]
    AWS_ACCESS_KEY_ID='***'
    AWS_SECRET_ACCESS_KEY='***'


## Test PySpark and S3 Bucket Access

Use the `test.py` file to verify reads from the `udacity-dend` bucket and writes to the S3 project bucket.

    spark-submit --master yarn test.py


## Run the Sparkify ETL Script

Confirm the `output_data_path` is configured for the current S3 project bucket.

    spark-submit --master yarn etl.py


## PySpark Links

Information on these pages was referenced while working on this project.

https://community.hortonworks.com/questions/226317/spark-read-from-different-account-s3-and-write-to.html

https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PySpark_Cheat_Sheet_Python.pdf

https://www.qubole.com/resources/pyspark-cheatsheet/

http://mail-archives.apache.org/mod_mbox/spark-user/201612.mbox/%3CCAFbeQtEuiioyjVy7PXfn9cXk_=ybq6hAK5ToHcmf85wPwmTbJA@mail.gmail.com%3E

https://stackoverflow.com/questions/52292180/pyspark-generate-row-hash-of-specific-columns-and-add-it-as-a-new-column


## Extra: Using docker to create local standalone Spark cluster

Run the following command to stand-up a local Spark cluster.

    bin/build_spark_image.sh
    bin/build_jupyter_image.sh
    bin/run_spark_stack.sh

Run the following command to download project data from the S3 bucket.

    aws s3 sync s3://udacity-dend/song_data ./data/song_data --no-sign-request
    aws s3 sync s3://udacity-dend/log_data ./data/log_data --no-sign-request


## Extra: Syncing data to an S3 bucket

The following commands will sync an entire local folder to an S3 bucket folder.

    aws s3 sync data/log_data/ s3://jlauman-project-04/log_data
    aws s3 sync data/song_data/ s3://jlauman-project-04/song_data


### Extra: Set Up Anaconda

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


## Extra: Copy Project's Jupyter Workspace

    zip -r workspace.zip workspace
    mv workspace.zip workspace_original.zip
    mv workspace_original.zip workspace
