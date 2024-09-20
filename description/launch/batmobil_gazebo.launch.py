from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    return LaunchDescription([
        # Launch Gazebo Simulator with an empty world or specify your world file
        ExecuteProcess(
            cmd=['gz', 'sim', '-v', '4'],  # Add '--render-engine ogre2' if needed for compatibility
            output='screen'
        ),

        # Load Robot State Publisher with your robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command(['xacro ', '/home/noi/pw2/src/RoboGardener/description/urdf/batmobil.urdf']),
                'use_sim_time': True  # Ensures the robot uses simulated time
            }]
        ),

        # Launch Joint State Publisher GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
            parameters=[{'use_sim_time': True}]  # Corrected the typo here ('use_sim_tim' to 'use_sim_time')
        ),

        # Launch RViz for robot visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', '/home/noi/pw2/src/RoboGardener/description/batmobil_config.rviz'],
            parameters=[{'use_sim_time': True}]
        ),
    ])
