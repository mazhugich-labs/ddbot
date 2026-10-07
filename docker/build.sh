#!/bin/bash

img_tag="${1:-latest}"

docker build \
    --build-arg USER_UID=$(id -u) \
    --build-arg USER_GID=$(id -g) \
    -t "$(basename $(pwd)):${img_tag}" .
