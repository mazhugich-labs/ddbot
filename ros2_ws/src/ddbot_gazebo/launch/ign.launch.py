#!/usr/bin/python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import AppendEnvironmentVariable


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    use_sim_time = LaunchConfiguration("use_sim_time", default=True)

    world_file_path = os.path.join(pkg_share, "worlds", "default.sdf")
    world_file = LaunchConfiguration("world_file", default=world_file_path)

    gz_sim_share = get_package_share_directory("ros_gz_sim")
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_sim_share, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": PythonExpression(["'", world_file, " -r'"])
        }.items(),
    )

    spawn_bcr_bot_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "ddbot_spawn.launch.py")
        ),
        launch_arguments={}.items(),
    )

    return LaunchDescription(
        [
            AppendEnvironmentVariable(
                name="IGN_GAZEBO_RESOURCE_PATH", value=os.path.join(pkg_share, "worlds")
            ),
            DeclareLaunchArgument("use_sim_time", default_value=use_sim_time),
            DeclareLaunchArgument("world_file", default_value=world_file),
            gz_sim,
            spawn_bcr_bot_node,
        ]
    )
