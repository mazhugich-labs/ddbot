import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_name = "ddbot_slam"
    pkg_share = get_package_share_directory(pkg_name)

    pkg_gazebo = "ddbot_gazebo"
    pkg_gazebo_share = get_package_share_directory(pkg_gazebo)
    ddbot_ign = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_share, "launch", "ign.launch.py")
        ),
        launch_arguments={
            "world_file": LaunchConfiguration("world_file"),
        }.items(),
    )

    ddbot_teleop = Node(
        package="ddbot_teleop",
        executable="ddbot_teleop",
        output="screen",
    )

    pkg_localization = "ddbot_localization"
    pkg_localization_share = get_package_share_directory(pkg_localization)
    ddbot_localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_localization_share, "launch", "ekf_local.launch.py")
        )
    )

    rviz2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_share, "launch", "rviz.launch.py")
        ),
        launch_arguments={
            "rviz2_cfg": os.path.join(pkg_share, "rviz", "cfg.rviz"),
            "use_sim_time": "true",
        }.items(),
    )

    ddbot_slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "slam.launch.py")
        ),
        launch_arguments={
            "set_localization_mode": LaunchConfiguration("set_localization_mode"),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("world_file", default_value="default.sdf"),
            DeclareLaunchArgument("set_localization_mode", default_value="false"),
            ddbot_ign,
            ddbot_teleop,
            ddbot_localization,
            ddbot_slam,
            rviz2,
        ]
    )
