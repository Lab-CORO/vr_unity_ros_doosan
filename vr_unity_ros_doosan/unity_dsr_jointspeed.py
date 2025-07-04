import rclpy
from rclpy.node import Node
from dsr_msgs2.msg import SpeedjRtStream
from std_msgs.msg import Float64MultiArray

# SpeedjRtStream
# vel float64[6] # [joint_1, joint_2, joint_3, joint_4, joint_5, joint_6] deg/s
# acc float64[6] # [joint_1, joint_2, joint_3, joint_4, joint_5, joint_6] deg/s^2
# time float64   # [s]
# source : https://manual.doosanrobotics.com/en/ros/2.00/Publish/speedlrtstream-msg

# std_msgs/Float64MultiArray
# data float64[] # Array of float64 values
# source : https://docs.ros.org/en/noetic/api/std_msgs/html/msg/Float64MultiArray.html


class Unity_Dsr2_msg(Node):
    def __init__(self):
        super().__init__('unity_dsr2_msg_j_node')
        # Initialisation du publisher
        self.speedj_rt_publisher = self.create_publisher(SpeedjRtStream, '/dsr01/speedj_rt_stream', 10)
        # Initialisation du subscriber
        self.jointspeed_subscriber = self.create_subscription(Float64MultiArray, '/unity/jointspeed', self.joint_callback, 10)

    def convert_twist_to_speedl(self, jointspeed):
        msg = SpeedjRtStream()
        msg.vel = [self.convert_rad_s_to_deg_s(jointspeed.data[0]),
                   self.convert_rad_s_to_deg_s(jointspeed.data[1]), 
                   self.convert_rad_s_to_deg_s(jointspeed.data[2]),
                   self.convert_rad_s_to_deg_s(jointspeed.data[3]), 
                   self.convert_rad_s_to_deg_s(jointspeed.data[4]), 
                   self.convert_rad_s_to_deg_s(jointspeed.data[5])]
        msg.acc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        msg.time = 0.04
        return msg
    
    def joint_callback(self, msg):
        speedj_msg = self.convert_twist_to_speedl(msg)
        self.speedj_rt_publisher.publish(speedj_msg)

    def convert_rad_s_to_deg_s(self, rad_s):
        return rad_s * (180.0 / 3.14159)

def main(args=None):
    rclpy.init(args=args)
    node = Unity_Dsr2_msg()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()