from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'vr_unity_ros_doosan'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='coro',
    maintainer_email='TODO@example.com',
    description='Unity-ROS2 bridge for Doosan robot integration.',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'unity_dsr_twist = vr_unity_ros_doosan.unity_dsr_twist:main',
            'unity_dsr_jointspeed = vr_unity_ros_doosan.unity_dsr_jointspeed:main',
        ],
    },
)
