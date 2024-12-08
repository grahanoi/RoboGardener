from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Path to the URDF/Xacro file
    urdf_file_path = '/home/noi/robogardener/scr/RoboGardener/model/description/robo.urdf.xacro'

    return LaunchDescription([
        # Node for robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_file_path])
            }]
        ),
        # Node for RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', '/home/noi/robogardener/scr/RoboGardener/model/config/batmobil_config.rviz']  # Path to your RViz config file
        ),
        
        # Node for MotorGui
        #Node(
        #    package='serial_motor_demo',
        #    executable='gui',
        #    name='motor_gui',
        #    output='screen'
        #),
        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),

        # Gazebo starten mit "gz sim"
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', 'empty.sdf'],
            output='screen'
        ),
        
        Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        arguments=[
            '-topic', '/robot_description',  # Beschreibung des Roboters
            '-name', 'batmobile'  # Name des Roboters in Gazebo
            ],
            output='screen',
        ),
        # Gazebo-ROS bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tf_bridge',
            arguments=[
                '/world/default/tf@tf2_msgs/msg/TFMessage[tf2_msgs/msg/TFMessage',
                '/world/default/odom@nav_msgs/msg/Odometry[nav_msgs/msg/Odometry'
            ],
            output='screen'
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['diff_cont'],
            output='screen',
        ),

        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_broad'],
            output='screen',
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_pub',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
            output='screen'
        ),
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            name='ros2_control_node',
            output='screen',
            parameters=[
                {'robot_description': Command(['xacro ', urdf_file_path])}
            ]
        ),


    ])
