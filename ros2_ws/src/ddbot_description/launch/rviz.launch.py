import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription
from launch.conditions import IfCondition


def generate_launch_description():
    pkg_name = "ddbot_description"
    pkg_share = get_package_share_directory(pkg_name)

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    launch_rsp = LaunchConfiguration("launch_rsp", default="true")
    launch_jsp = LaunchConfiguration("launch_jsp", default="true")

    xacro_description = os.path.join(pkg_share, "urdf", "ddbot.xacro")
    robot_description = Command(["xacro ", xacro_description])
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name=f"{pkg_name}_robot_state_publisher",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_description": robot_description,
            },
        ],
        condition=IfCondition(launch_rsp),
    )

    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name=f"{pkg_name}_joint_state_publisher",
        condition=IfCondition(launch_jsp),
    )

    rviz2_config = os.path.join(pkg_share, "rviz", "config.rviz")
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name=f"{pkg_name}_rviz2",
        output="screen",
        arguments=["-d", rviz2_config],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation time if true",
            ),
            DeclareLaunchArgument(
                "launch_rsp",
                default_value="true",
                description="Disable robot state publisher if false",
            ),
            DeclareLaunchArgument(
                "launch_jsp",
                default_value="true",
                description="Disable joint state publisher if false",
            ),
            robot_state_publisher,
            joint_state_publisher,
            rviz2,
        ]
    )
