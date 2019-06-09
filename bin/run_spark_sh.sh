#!/usr/bin/env bash

# the "-l" maks sh a login shell (so /etc/profile is sourced)
docker run --rm -it --net sparknet local:spark /bin/sh -l
