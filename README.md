# Project 4: Data Lake

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

    conda create --name dend_project_04 python=3.7
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
