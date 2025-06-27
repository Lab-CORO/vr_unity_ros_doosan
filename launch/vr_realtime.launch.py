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


# <!-- <launch>

#     <!-- Add the ros_unity_fixed_rate_pointcloud2 script-->
#     <node pkg="unity_ros_doosan" name="fixed_rate_pointcloud2" type="ros_unity_fixed_rate_pointcloud2.py"/>
#     <!-- Add the unity_moveit_twist script-->
#     <node pkg="unity_ros_doosan" name="unity_moveit_twist" type="unity_moveit_twist.py"/>
#     <!-- Add the gripper_control script-->
#     <node pkg="unity_ros_doosan" name="gripper_control" type="gripper_control.py"/>

#     <!-- Add the Realsense camera launch-->
#     <include file="$(find realsense2_camera)/launch/rs_camera.launch">
#         <arg name="filters"         value="pointcloud"/>
#         <!-- <arg name="enable_infra"    value="true"/> -->

#         <!-- 424 -->
#         <arg name="color_width"     value="424"/>
#         <arg name="depth_width"     value="424"/>
#         <arg name="infra_width"     value="424"/>

#         <!-- 240 -->
#         <arg name="color_height"    value="240"/>
#         <arg name="depth_height"    value="240"/>
#         <arg name="infra_height"    value="240"/>

#         <arg name="color_fps"       value="30"/>
#         <arg name="depth_fps"       value="30"/>
#         <arg name="infra_fps"       value="30"/>
#     </include>

#     <!-- Add the ros_tcp_endpoint launch-->
#     <!-- <include file="$(find ros_tcp_endpoint)/launch/endpoint.launch"/> -->

#     <!-- Add the robotiq_85_driver script-->
#     <node pkg="robotiq_85_driver" name="robotiq_driver" type="robotiq_85_driver"/>

# </launch> -->