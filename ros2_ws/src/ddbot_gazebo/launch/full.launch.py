import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "ign.launch.py")
        ),
        launch_arguments={}.items(),
    )

    rviz2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "rviz.launch.py")
        ),
        launch_arguments={}.items(),
    )

    ddbot_teleop_gui = Node(
        package="ddbot_teleop_gui",
        executable="ddbot_teleop_gui",
        output="screen",
    )

    return LaunchDescription([gz_sim, rviz2, ddbot_teleop_gui])
