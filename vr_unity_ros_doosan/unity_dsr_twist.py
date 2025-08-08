import rclpy
from rclpy.node import Node
from dsr_msgs2.msg import SpeedlRtStream
from geometry_msgs.msg import Twist

# SpeedlRtStream
# vel float64[6] # [vx, vy, vz, wx, wy, wz]
# acc float64[6] # [ax, ay, az, awx, awy, awz]
# time float64   # [s]
# source : https://manual.doosanrobotics.com/en/ros/2.00/Publish/speedlrtstream-msg

# Geometry_msgs/Twist
# linear Vector3
#   x float64
#   y float64
#   z float64
# angular Vector3
#   x float64
#   y float64
#   z float64
# source :
# Vector3: https://docs.ros2.org/galactic/api/geometry_msgs/msg/Vector3.html
#   Twist: https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html

class Unity_Dsr2_msg(Node):
    def __init__(self):
        super().__init__('unity_dsr2_msg_node')

        # Initialisation du publisher
        self.speedl_rt_publisher = self.create_publisher(SpeedlRtStream, '/dsr01/speedl_rt_stream', 10)
        # Initialisation du subscriber
        self.twist_subscriber = self.create_subscription(Twist, '/unity/twist', self.twist_callback, 10)

    def convert_twist_to_speedl(self, twist):
        msg = SpeedlRtStream()
        msg.vel = [max(min(twist.linear.x*1000, 250),-250),
                   max(min(twist.linear.y*1000, 250),-250),
                   max(min(twist.linear.z*1000, 250),-250),
                   max(min(twist.angular.x*(180.0 / 3.14159), 30),-30),
                   max(min(twist.angular.y*(180.0 / 3.14159), 30),-30), 
                   max(min(twist.angular.z*(180.0 / 3.14159), 30),-30)]
        msg.acc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

         # 0.04 corresponds to the message frequency of a previous Carl's project. 
         # This value could potentially be lowered, but 0.04s is working just fine.
        msg.time = 0.04
        return msg
    
    def twist_callback(self, msg):
        speedl_msg = self.convert_twist_to_speedl(msg)
        self.speedl_rt_publisher.publish(speedl_msg)


def main(args=None):
    rclpy.init(args=args)
    node = Unity_Dsr2_msg()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()