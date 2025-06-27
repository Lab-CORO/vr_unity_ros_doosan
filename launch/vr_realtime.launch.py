from launch import LaunchDescription
from launch_ros.actions import Node, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Path to the Realsense launch file
    realsense_launch_path = os.path.join(
        FindPackageShare('realsense2_camera').find('realsense2_camera'),
        'launch',
        'rs_camera.launch.py'  # A voir quel est le nom du launch file
    )

    return LaunchDescription([
        # Conversion twist to dsr node
        Node(
            package='vr_unity_ros_doosan',
            executable='unity_dsr_twist.py',
            name='unity_dsr_twist',
            output='screen'
        ),
    
        # # Realsense launch include
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(realsense_launch_path),
        #     launch_arguments=[
        #         ('filters', 'pointcloud'),
        #         ('color_width', '424'),
        #         ('depth_width', '424'),
        #         ('infra_width', '424'),
        #         ('color_height', '240'),
        #         ('depth_height', '240'),
        #         ('infra_height', '240'),
        #         ('color_fps', '30'),
        #         ('depth_fps', '30'),
        #         ('infra_fps', '30')
        #     ]
        # ),
    ])
