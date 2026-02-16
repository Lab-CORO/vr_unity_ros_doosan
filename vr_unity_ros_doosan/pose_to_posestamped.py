import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseStamped, TransformStamped
from tf2_ros import TransformBroadcaster


class PoseToPoseStamped(Node):

    def __init__(self):
        super().__init__('pose_to_posestamped')

        self.declare_parameter('frame_id', 'base_link')
        self.declare_parameter('child_frame_id', 'mpc_goal')
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        self.child_frame_id = self.get_parameter('child_frame_id').get_parameter_value().string_value

        self.sub = self.create_subscription(
            Pose, 'unified_planner/mpc_goal', self.pose_callback, 10)

        self.pub = self.create_publisher(
            PoseStamped, 'unified_planner/mpc_goal_stamped', 10)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info(
            f'Converting Pose -> PoseStamped + TF (frame: {self.frame_id} -> {self.child_frame_id})')

    def pose_callback(self, msg: Pose):
        now = self.get_clock().now().to_msg()

        stamped = PoseStamped()
        stamped.header.stamp = now
        stamped.header.frame_id = self.frame_id
        stamped.pose = msg
        self.pub.publish(stamped)

        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = self.frame_id
        t.child_frame_id = self.child_frame_id
        t.transform.translation.x = msg.position.x
        t.transform.translation.y = msg.position.y
        t.transform.translation.z = msg.position.z
        t.transform.rotation = msg.orientation
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = PoseToPoseStamped()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
