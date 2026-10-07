#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    # Launch configurations
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    # Process XACRO
    xacro_description = os.path.join(pkg_share, "urdf", "ddbot.xacro")
    robot_description = Command(
        [
            "xacro ",
            xacro_description,
            " wheel_odom_topic:=",
            "odom",
        ]
    )

    # Nodes
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"use_sim_time": use_sim_time},
            {"robot_description": robot_description},
        ],
    )

    rvi2_config = os.path.join(pkg_share, "rviz", "config.rviz")
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rvi2_config],
    )

    return LaunchDescription(
        [
            # Declare arguments
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation time if true",
            ),
            # Nodes
            robot_state_publisher,
            rviz2,
        ]
    )
