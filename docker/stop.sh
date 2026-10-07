#1/bin/bash

ctr_tag="${1:-latest}"

docker stop "$(basename $(pwd))-${ctr_tag}"
