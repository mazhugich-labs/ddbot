import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "ign.launch.py")
        ),
        launch_arguments={
            "use_sim_time": "true",
            "world_file": LaunchConfiguration("world_file"),
        }.items(),
    )

    rviz2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "rviz.launch.py")
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    ddbot_teleop = Node(
        package="ddbot_teleop",
        executable="ddbot_teleop",
        output="screen",
    )

    odom = Node(
        package="odom_to_tf_ros2",
        executable="odom_to_tf",
        name="odom_to_tf",
        output="screen",
        parameters=[
            {
                "odom_topic": "/ddbot/wheel/odom",
                "frame_id": "odom",
                "child_frame_id": "base_footprint",
                "inverse_tf": False,
            }
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("world_file", default_value="default.sdf"),
            gz_sim,
            rviz2,
            ddbot_teleop,
            odom,
        ]
    )
