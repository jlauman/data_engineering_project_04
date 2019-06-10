#!/usr/bin/env bash

docker build --tag local:jupyter --file - ./ <<EOF
FROM centos:centos7

RUN yum -y install epel-release &&\
    yum -y update &&\
    yum -y install java-1.8.0-openjdk &&\
    yum -y install sudo ack wget curl bzip2

COPY ./etc/alias.sh ./etc/conda.sh /etc/profile.d/

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda &&\
    /root/miniconda/bin/conda create -y -n project python=3.7 jupyterlab pandas pyspark &&\
    /root/miniconda/bin/conda init bash

CMD [ "/bin/bash" ]

EOF
