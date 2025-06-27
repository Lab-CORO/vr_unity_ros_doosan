from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'vr_unity_ros_doosan'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='coro',
    maintainer_email='   TODO   ',
    description='unity_ros_doosan package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            
        ],
    },
)
