#!/bin/bash
set -e

colcon build --symlink-install
echo "source $(pwd)/install/setup.bash" >> $HOME/.bashrc

exec "$@"
