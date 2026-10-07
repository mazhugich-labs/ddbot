#!/bin/bash

img_tag="${1:-latest}"
ctr_tag="${2:-latest}"

xhost +local:root

docker run -dit --rm \
    --name "$(basename $(pwd))-${ctr_tag}" \
    --gpus all \
    --device=/dev/dri:/dev/dri \
    --group-add 44 \
    --group-add 990 \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="NVIDIA_DRIVER_CAPABILITIES=all" \
    --env="__NV_PRIME_RENDER_OFFLOAD=1" \
    --env="__GLX_VENDOR_LIBRARY_NAME=nvidia" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --net=host \
    -v ./ros2_ws:/home/ros2_ws \
    "$(basename $(pwd)):${img_tag}"
