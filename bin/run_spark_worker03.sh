#!/usr/bin/env bash

docker run \
    --name worker03 \
    --net sparknet \
    --rm \
    --detach \
    local:spark \
    /usr/sbin/sshd -D
