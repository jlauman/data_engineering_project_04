#!/usr/bin/env bash

# jupyter lab --notebook-dir=.

docker run \
    --name jupyter \
    --net sparknet \
    --publish 8888:8888 \
    --mount type=bind,source="$(pwd)/workspace",target=/opt/workspace \
    --rm \
    --detach \
    local:jupyter \
    /root/miniconda/bin/conda run -n project jupyter lab --notebook-dir=/opt/workspace --no-browser --ip=jupyter --allow-root --NotebookApp\.token=''

# /bin/sh -l
