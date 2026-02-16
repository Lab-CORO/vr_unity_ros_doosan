#!/usr/bin/env python3
"""
Gripper Bridge Node
Simplified interface between Unity and Robotiq 85 Gripper
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from robotiq_85_msgs.msg import GripperCmd, GripperStat


class GripperBridge(Node):
    def __init__(self):
        super().__init__('gripper_bridge')

        # Parameters (can be modified via launch file or command line)
        self.declare_parameter('default_speed', 0.1)  # Default gripper speed
        self.declare_parameter('default_force', 50.0)  # Default gripper force
        self.declare_parameter('position_threshold', 0.001)  # Minimum change to publish (in meters, ~1mm)

        self.default_speed = self.get_parameter('default_speed').value
        self.default_force = self.get_parameter('default_force').value
        self.position_threshold = self.get_parameter('position_threshold').value

        # Track last published position to avoid spamming
        self.last_published_position = None

        # Publisher: Send commands to gripper
        self.gripper_cmd_pub = self.create_publisher(
            GripperCmd,
            '/gripper/cmd',
            10
        )

        # Publisher: Send gripper position to Unity
        self.unity_stat_pub = self.create_publisher(
            Float32,
            '/unity/gripper_stat',
            10
        )

        # Subscriber: Receive control commands from Unity
        self.unity_control_sub = self.create_subscription(
            Float32,
            '/unity/control_gripper',
            self.unity_control_callback,
            10
        )

        # Subscriber: Receive gripper status
        self.gripper_stat_sub = self.create_subscription(
            GripperStat,
            '/gripper/stat',
            self.gripper_stat_callback,
            10
        )

        self.get_logger().info('Gripper Bridge Node started')
        self.get_logger().info(f'Default speed: {self.default_speed}, Default force: {self.default_force}')

    def unity_control_callback(self, msg: Float32):
        """
        Receive position command from Unity and send to gripper

        Args:
            msg (Float32): Gripper position (0.0 = fully open, 85.0 = fully closed for Robotiq 85)
        """
        # Create gripper command message
        cmd = GripperCmd()
        cmd.position = float((msg.data * 0.085)/100.0)
        cmd.speed = self.default_speed
        cmd.force = self.default_force
        cmd.emergency_release = False
        cmd.emergency_release_dir = 0
        cmd.stop = False

        # Publish command
        self.gripper_cmd_pub.publish(cmd)

        self.get_logger().info(
            f'Gripper command sent: position={cmd.position:.2f}, '
            f'speed={cmd.speed:.2f}, force={cmd.force:.2f}'
        )

    def gripper_stat_callback(self, msg: GripperStat):
        """
        Receive gripper status and republish only position to Unity
        Only publishes when position changes significantly to avoid spamming

        Args:
            msg (GripperStat): Full gripper status
        """
        current_position = msg.position

        # Check if this is first message or if position changed significantly
        if (self.last_published_position is None or
            abs(current_position - self.last_published_position) >= self.position_threshold):

            # Extract position and publish to Unity
            position_msg = Float32()
            position_msg.data = current_position

            self.unity_stat_pub.publish(position_msg)

            # Update last published position
            self.last_published_position = current_position

            self.get_logger().debug(
                f'Gripper position published: {current_position:.4f} '
                f'(is_moving={msg.is_moving}, obj_detected={msg.obj_detected})'
            )


def main(args=None):
    rclpy.init(args=args)

    node = GripperBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
