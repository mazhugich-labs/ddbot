from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    pkg_name = "ddbot_localization"
    pkg_share = get_package_share_directory(pkg_name)

    ekf_config = os.path.join(pkg_share, "config", "ekf.yaml")

    ekf_map = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node_map",
        output="screen",
        parameters=[ekf_config, {"use_sim_time": True}],
        remappings=[("odometry/filtered", "odometry/global")],
    )

    ekf_navsat = Node(
        package="robot_localization",
        executable="navsat_transform_node",
        name="navsat_transform",
        output="screen",
        parameters=[ekf_config, {"use_sim_time": True}],
        remappings=[
            ("imu", "/ddbot/imu"),
            ("gps/fix", "/ddbot/navsat"),
            ("odometry/filtered", "/odometry/global"),
            ("odometry/gps", "/odometry/gps"),
            ("gps/filtered", "/gps/filtered"),
        ],
    )

    return LaunchDescription(
        [
            ekf_map,
            ekf_navsat,
        ]
    )
