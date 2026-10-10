#!/usr/bin/python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import (
    PythonExpression,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import AppendEnvironmentVariable


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    world_file_path = PathJoinSubstitution(
        [pkg_share, "worlds", LaunchConfiguration("world_file")]
    )

    gz_sim_share = get_package_share_directory("ros_gz_sim")
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_sim_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": PythonExpression(["'", world_file_path, " -r'"])
        }.items(),
    )

    spawn_bcr_bot_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "_ddbot_ign_spawn.launch.py")
        ),
        launch_arguments={
            "ground_truth_odom": LaunchConfiguration("ground_truth_odom"),
        }.items(),
    )

    return LaunchDescription(
        [
            AppendEnvironmentVariable(
                name="IGN_GAZEBO_RESOURCE_PATH", value=os.path.join(pkg_share, "worlds")
            ),
            DeclareLaunchArgument("world_file", default_value="default.sdf"),
            DeclareLaunchArgument("ground_truth_odom", default_value="false"),
            gz_sim,
            spawn_bcr_bot_node,
        ]
    )
