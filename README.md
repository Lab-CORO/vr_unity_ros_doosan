# ROS Project: Control Layer Between Unity and Doosan Robotic Arm

## Project Overview

This project aims to create a control layer between a Unity VR project and the ROS drivers of a Doosan robotic arm. It enables seamless communication between Unity and ROS, allowing real-time control and manipulation of the robotic arm using VR inputs.

## Features
- Control layer transforming messages for communication between Unity and ROS.
- Support for Doosan robotic arm with ROS drivers.
- Real-time control using Unity VR and ROS.

## Installation Instructions

This project cannot function independently, as some launch files require other projects.

### Prerequisites

- **Operating System**: This project was developed using ROS Humble on Ubuntu 20.04.
- **Doosan robot**: The scripts in this project work with the ROS Doosan drivers available [here](https://github.com/ETS-J-Boutin/doosan-robot_RT), a modified version of the [original](https://github.com/BryanStuurman/doosan-robot) branch. For detailed setup instructions, refer to this [issue](https://github.com/doosan-robotics/doosan-robot/issues/99).
- **Unity-ROS Bridge**: This can be found at the [Lab-CoRo](https://github.com/Lab-CORO/ROS-TCP-Endpoint.git) and is used to connect Unity to ROS. For tutorials and guidance on setting up ROS2 in Unity, follow their [ROS_setup tutorial](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials). Be warned, most of the tutorials offered are using ROS1 and not ROS2.

By adding these to your in your workspace, you should have, including this project, a folder for the following projects:
- Doosan robot
- ROS TCP Endpoint
- VR Unity ROS Doosan (this project)

Make sure to run `colcon build` after all these installations.

## From a clean install
Specific information if you're trying this project from a clean install.

- Install [ROS Humble (desktop)](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) by following the tutorial.
- Import the [Leeloo-Docker](https://github.com/Lab-CORO/leeloo.git) from the vr-leeloo branch. The `Leeloo-Docker` includes the packages
  for the `Doosan robot` the `Unity-ROS Bridge` and this project.

## Usage

These are the commands you might want to run.

### Roslaunch

- **vr_realtime.launch**: Starts the nodes responsbible for the conversion of units from Unity to the Doosan Robot: `unity_dsr_twist & unity_dsr_jointspeed`. Enables real-time communication between the Unity VR interface and ROS2 with the `TCP server`.

### Example

Launch the various ROS components needed for real-time manipulation using the following commands in multiple command windows:

  ```bash
  ros2 launch leeloo bringup_leeloo.launch # Launch the Doosan bringup launch file and the robot segmentation from the curobo package
  ros2 launch vr_unity_ros_doosan vr_realtime.launch #  Launch used for the realtime manipulation of the robot via Unity
```

## Known Issues and Possible Fix

While running the `ROS-TCP-Endpoint` package from the launch command `ros2 launch vr_unity_ros_doosan vr_realtime.launch`, an error can occur indicating that the TCP server is unable to start. This is likely due to the specified `ROS_TCP_PORT` already being in use, which suggests that another instance of the `default_server_endpoint` node is already running. As a result, Unity is unable to establish a new TCP connection to ROS2. This issue is caused by starting/stopping the VR interface too many times in a short period. 
To fix this issue, kill the launch file, restart the docker and run the launch command again.