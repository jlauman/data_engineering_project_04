#!/usr/bin/env bash

docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 sparknet

docker build --tag local:spark --file - ./ <<EOF
FROM centos:centos7

RUN yum -y install epel-release &&\
    yum -y update &&\
    yum -y install openssh-server openssh-clients &&\
    yum -y install java-1.8.0-openjdk &&\
    yum -y install ack wget curl &&\
    wget https://downloads.lightbend.com/scala/2.11.12/scala-2.11.12.rpm &&\
    yum -y install scala-2.11.12.rpm

RUN wget http://apache.cs.utah.edu/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz &&\
    tar xzf spark-2.4.3-bin-hadoop2.7.tgz &&\
    mv spark-2.4.3-bin-hadoop2.7 /usr/local/spark

RUN ssh-keygen -N '' -t dsa -f /etc/ssh/ssh_host_dsa_key &&\
    ssh-keygen -N '' -t rsa -f /etc/ssh/ssh_host_rsa_key &&\
    ssh-keygen -N '' -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key &&\
    ssh-keygen -N '' -t ed25519 -f /etc/ssh/ssh_host_ed25519_key

COPY ./etc/alias.sh ./etc/spark.sh /etc/profile.d/

COPY ./etc/id_rsa ./etc/id_rsa.pub /root/.ssh/
COPY ./etc/id_rsa.pub /root/.ssh/authorized_keys

RUN rm -rf /root/.ssh/known_hosts &&\
    touch /root/.ssh/known_hosts &&\
    echo "worker01 \$(cat /etc/ssh/ssh_host_ecdsa_key.pub)" >> /root/.ssh/known_hosts &&\
    echo "worker02 \$(cat /etc/ssh/ssh_host_ecdsa_key.pub)" >> /root/.ssh/known_hosts &&\
    echo "worker03 \$(cat /etc/ssh/ssh_host_ecdsa_key.pub)" >> /root/.ssh/known_hosts

COPY ./etc/slaves /usr/local/spark/conf/slaves
COPY ./etc/spark-env.sh /usr/local/spark/conf/spark-env.sh

CMD [ "/bin/sh" ]

EOF
