# -----------------------------------------------------------------------------
# ROS 2 Node: PauseResumeTopicBridge
#
# Description:
# This ROS 2 node acts as a bridge between a Unity simulation and the doosan's 
# motion control services. It listens for Boolean messages published on the 
# topic `/unity/UnityPauseResume`. Depending on the message content, it sends 
# a request to either pause or resume the robot's motion. This node is used
# as Deadman switch similar to the Doosan robot. 
#
# Functionality:
# - If the received message is 'False', the node sends a request to the 
#   '/dsr01/motion/move_pause' service to pause the robot.
# - If the received message is 'True', the node sends a request to the 
#   '/dsr01/motion/move_resume' service to resume the robot.
#
# Services:
# - /dsr01/motion/move_pause (type: dsr_msgs2/srv/MovePause)
# - /dsr01/motion/move_resume (type: dsr_msgs2/srv/MoveResume)
#
# The node handles service responses asynchronously and logs the result of 
# each command.
# -----------------------------------------------------------------------------

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from dsr_msgs2.srv import MovePause, MoveResume


class PauseResumeTopicBridge(Node):
    def __init__(self):
        super().__init__('pause_resume_topic_bridge')

        self.sub = self.create_subscription( Bool,'/unity/UnityPauseResume',self.callback,10)
        self.get_logger().info("Subscribed to /UnityPauseResume")

        self.pause_client = self.create_client(MovePause, '/dsr01/motion/move_pause')
        self.resume_client = self.create_client(MoveResume, '/dsr01/motion/move_resume')

        while not self.pause_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for /move_pause service...")
        while not self.resume_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for /move_resume service...")

    def callback(self, msg):
        if msg.data is False:
            self.get_logger().info("Received PAUSE command from Unity")
            req = MovePause.Request()
            future = self.pause_client.call_async(req)
            self._handle_future(future, "Pause")

        elif msg.data is True:
            self.get_logger().info("Received RESUME command from Unity")
            req = MoveResume.Request()
            future = self.resume_client.call_async(req)
            self._handle_future(future, "Resume")

    # The purpose of the _handle_future function is to create an asynchronous service call response without blocking the node's main execution
    # The done_callback function is used to display a success or an error message when the response is issued (e.g. Success or Failure)
    def _handle_future(self, future, label):
        def done_callback(futur_response):
            result = futur_response.result()
            if result is not None and getattr(result, 'success', False): 
                self.get_logger().info(f"{label} Command succeeded!")
            else:
                self.get_logger().error(f"{label} Command failed or returned no result.")

        future.add_done_callback(done_callback)


def main(args=None):
    rclpy.init(args=args)
    node = PauseResumeTopicBridge()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
