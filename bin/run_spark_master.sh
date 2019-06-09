#!/usr/bin/env bash

docker run \
    --name master \
    --net sparknet \
    --publish 4040:4040 \
    --publish 8080:8080 \
    --rm \
    --detach \
    local:spark \
    /usr/local/spark/sbin/start-all.sh

# /bin/sh -l
