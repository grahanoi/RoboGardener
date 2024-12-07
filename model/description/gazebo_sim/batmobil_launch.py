import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Directories for packages and models
    pkg_project_description = get_package_share_directory('robogardener')
    sdf_file_path = os.path.join(pkg_project_description, 'description', 'gazebo_sim', 'batmobil_world.sdf')

    # Load the SDF file for the robot
    with open(sdf_file_path, 'r') as sdf_file:
        robot_desc = sdf_file.read()

    # Declare Launch Arguments
    declare_rviz_arg = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='Flag to enable RViz visualization'
    )

    # Joint State Publisher GUI Node
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc}
        ],
        output='screen'
    )

    # RViz Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_project_description, 'config', 'batmobil.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz'))
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
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
        gazebo_launch
    ])
