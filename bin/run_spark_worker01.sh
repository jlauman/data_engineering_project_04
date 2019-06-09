#!/usr/bin/env bash

docker run \
    --name worker01 \
    --net sparknet \
    --rm \
    --detach \
    local:spark \
    /usr/sbin/sshd -D

# --restart unless-stopped \
# --rm -it \
# --detach \
# /bin/sh -l
