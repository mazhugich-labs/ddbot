import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_name = "ddbot_localization"
    pkg_share = get_package_share_directory(pkg_name)

    ekf_local = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "ekf_local.launch.py")
        )
    )

    ekf_global = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "ekf_global.launch.py")
        )
    )

    return LaunchDescription([ekf_local, ekf_global])
