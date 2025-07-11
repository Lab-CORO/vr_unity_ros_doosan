from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():

    return LaunchDescription([
        
        Node(
            package='vr_unity_ros_doosan',
            executable='unity_dsr_twist', 
            name='unity_dsr_twist',
            output='screen'
        ),

        Node(
            package='vr_unity_ros_doosan',
            executable='unity_dsr_jointspeed',
            name='unity_dsr_jointspeed',
            output='screen'  
        ),
    
        Node(
            package='ros_tcp_endpoint',
            executable='default_server_endpoint',
            name='default_server_endpoint',
            output='screen',
            parameters=[{'ROS_IP': '0.0.0.0', 'ROS_TCP_PORT': 10000}]
        ),

    ])
