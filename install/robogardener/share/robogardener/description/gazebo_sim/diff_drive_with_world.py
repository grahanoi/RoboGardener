import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Path to the SDF file
    pkg_project_description = get_package_share_directory('robogardener')
    sdf_file_path = os.path.join(pkg_project_description, 'description', 'gazebo_sim', 'batmobil_world.sdf')

    # Declare Launch Arguments
    declare_rviz_arg = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='Flag to enable RViz visualization'
    )

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': open(sdf_file_path, 'r').read()}  # Ensure this is only for the robot model part
        ],
        output='screen'
    )

        # Joint State Publisher GUI Node
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Bridge between Gazebo and ROS for TF and topics
    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist[ignition.msgs.Twist',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/tf_static@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model'
        ],
        output='screen'
    )

    # RViz Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_project_description, 'config', 'batmobil.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz')),
        output='screen'
    )

    # Launch Gazebo with the SDF file
    gazebo_launch = ExecuteProcess(
        cmd=[
            'gz', 'sim',
            sdf_file_path
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_rviz_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        ros_gz_bridge_node,
        rviz_node,
        gazebo_launch
    ])
