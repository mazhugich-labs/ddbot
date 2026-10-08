#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    # Process XACRO
    xacro_description = os.path.join(pkg_share, "urdf", "ddbot.xacro")
    robot_description = Command(["xacro ", xacro_description])

    # Nodes
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
            {"robot_description": robot_description},
        ],
    )

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz2_cfg")],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_sim_time", default_value="false"),
            DeclareLaunchArgument(
                "rviz2_cfg",
                default_value=os.path.join(pkg_share, "rviz", "config.rviz"),
            ),
            robot_state_publisher,
            rviz2,
        ]
    )
