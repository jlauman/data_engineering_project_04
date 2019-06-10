# Project 4: Data Lake

bin/build_spark_image.sh
bin/build_jupyter_image.sh
bin/run_spark_stack.sh


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


### Run Jupyter Labs

    bin/run_jupyter.sh


## Extra: Copy Project's Jupyter Workspace

    zip -r workspace.zip workspace
    mv workspace.zip workspace_original.zip
    mv workspace_original.zip workspace
