#!/usr/bin/env bash

docker run \
    --name worker02 \
    --net sparknet \
    --rm \
    --detach \
    local:spark \
    /usr/sbin/sshd -D
