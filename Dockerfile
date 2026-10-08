ARG ROS_DISTRO=humble
FROM osrf/ros:$ROS_DISTRO-desktop-full AS base

# FROM base AS det_tools

# RUN apt-get update && apt-get install -y \
#     ros-$ROS_DISTRO-ros-dev-tools

FROM base AS user_setup

ARG USERNAME=ros2_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Delete user if it exists in container (e.g Ubuntu Noble: ubuntu)
RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

FROM user_setup AS dependencies

RUN apt-get update && apt-get install -y \
    ros-$ROS_DISTRO-joint-state-publisher \
    ros-$ROS_DISTRO-joint-state-publisher-gui \
    ros-$ROS_DISTRO-rviz-imu-plugin \
    ros-$ROS_DISTRO-rviz-satellite \
    ros-$ROS_DISTRO-ros2-control \
    ros-$ROS_DISTRO-ros2-controllers \
    ros-$ROS_DISTRO-slam-toolbox \
    ros-$ROS_DISTRO-robot-localization

RUN apt-get update && apt-get install -y \
    mesa-utils

FROM dependencies AS final

RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /home/$USERNAME/.bashrc

USER $USERNAME

WORKDIR /home/ros2_ws

ENTRYPOINT [""]
CMD ["/bin/bash"]
