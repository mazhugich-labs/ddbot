import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction


def launch_setup(context, *args, **kwargs):
    pk_name = "ddbot_slam"
    pkg_share = get_package_share_directory(pk_name)

    slam_params = os.path.join(pkg_share, "config", "slam.yaml")

    localization_mode = (
        LaunchConfiguration("set_localization_mode").perform(context).lower() == "true"
    )

    executable = (
        "localization_slam_toolbox_node"
        if localization_mode
        else "async_slam_toolbox_node"
    )

    return [
        Node(
            package="slam_toolbox",
            executable=executable,
            name="slam_toolbox",
            output="screen",
            parameters=[slam_params, {"use_sim_time": True}],
            # remappings=[("scan", "/ddbot/scan")],
        )
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "set_localization_mode",
                default_value="false",
                description="Run SLAM Toolbox in localization mode",
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
