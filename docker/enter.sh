#!/bin/bash

ctr_tag="${1:-latest}"

docker exec -it "$(basename $(pwd))-${ctr_tag}" bash
