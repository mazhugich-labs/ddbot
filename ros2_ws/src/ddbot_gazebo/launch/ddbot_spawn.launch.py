import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription


def generate_launch_description():
    pkg_name = "ddbot_gazebo"
    pkg_share = get_package_share_directory(pkg_name)

    odometry_source = LaunchConfiguration("odometry_source")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[
            {
                "robot_description": Command(
                    [
                        "xacro ",
                        os.path.join(pkg_share, "urdf/ddbot.xacro"),
                        " odometry_source:=",
                        odometry_source,
                    ]
                )
            }
        ],
        remappings=[
            ("/joint_states", "ddbot/joint_states"),
        ],
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "/robot_description",
            "-name",
            "ddbot",
            "-allow_renaming",
            "true",
            "-z",
            "0.24",
            "-Y",
            "3.14",
        ],
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist",
            "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
            "/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry",
            "/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V",
            "/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/ultrasonic/front@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/ultrasonic/left@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/ultrasonic/rear@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/ultrasonic/right@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan",
            "/rgbd_camera@sensor_msgs/msg/Image[ignition.msgs.Image",
            "rgbd_camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo",
            "/rgbd_camera/points@sensor_msgs/msg/PointCloud2[ignition.msgs.PointCloudPacked",
            "/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU",
            "/world/default/model/ddbot/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model",
            "/navsat@sensor_msgs/msg/NavSatFix[ignition.msgs.NavSat",
        ],
        remappings=[
            ("/world/default/model/ddbot/joint_state", "ddbot/joint_states"),
            ("/odom", "ddbot/odom"),
            ("/scan", "ddbot/scan"),
            ("/ultrasonic/front", "ddbot/ultrasonic/front"),
            ("/ultrasonic/left", "ddbot/ultrasonic/left"),
            ("/ultrasonic/rear", "ddbot/ultrasonic/rear"),
            ("/ultrasonic/right", "ddbot/ultrasonic/right"),
            ("/rgbd_camera", "ddbot/rgbd_camera"),
            ("/imu", "ddbot/imu"),
            ("/cmd_vel", "ddbot/cmd_vel"),
            ("rgbd_camera/camera_info", "ddbot/rgbd_camera/camera_info"),
            ("/rgbd_camera/points", "ddbot/rgbd_camera/points"),
            ("/navsat", "ddbot/navsat"),
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("odometry_source", default_value="world"),
            robot_state_publisher,
            gz_spawn_entity,
            gz_ros2_bridge,
        ]
    )
