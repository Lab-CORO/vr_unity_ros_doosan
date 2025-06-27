#!/usr/bin/env python3

# ROS 2 node that moves a Doosan robot to a predefined home position using the MoveJoint service.
# The node connects to the motion service, builds a request with joint angles and motion parameters.

import rclpy
from rclpy.node import Node
from dsr_msgs2.srv.motion import MoveJoint 


# MoveJoint
# The robot moves to the target joint position (pos) from the current joint position.
#
# float64[6] pos               # target joint angle list [degree] 
# float64    vel               # set velocity: [deg/sec]
# float64    acc               # set acceleration: [deg/sec2]
# float64    time #= 0.0       # Time [sec] 
# float64    radius #=0.0      # Radius under blending mode [mm] 
# int8       mode #= 0         # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1 
# int8       blend_type #= 0    # BLENDING_SPEED_TYPE_DUPLICATE=0, BLENDING_SPEED_TYPE_OVERRIDE=1
# int8       sync_type #=0      # SYNC = 0, ASYNC = 1
# ---
# bool success

# source : https://github.com/DoosanRobotics/doosan-robot2/blob/humble/dsr_msgs2/srv/motion/MoveJoint.srv    


class MoveHomeNode(Node) :
    
        def __init__(self):
            super().__init__('move_home_client_node')

            # Create a client to the MoveJoint service 
            self.client = self.create_client = (MoveJoint,'/dsr_msgs2/srv/motion/MoveJoint')

            # Wait until the service is available
            while not self.client.wait_for_service(timeout_sec = 1.0):
                self.get_logger().info('The MoveJoint service is not available, waiting again...')

            # Sets the home position
            self.home_position = [0,-25,90,0,90,-90]

            # Calls the service
            self.call_move_joint(self.home_position)

        # Function that builds the request and send a MoveJoint request to move the robot 
        # to the Home position
        def call_move_joint(self,positions) :
            request = MoveJoint.Request()
            
            request.pos = positions
            request.vel = 15.0
            request.acc = 0.0
            request.time = 0.0
            request.radius = 0.0
            request.mode = 0
            request.blend_type = 0
            request.sync_type = 0
            

            self.get_logger().info (f'Moving to: {positions}')
            futur = self.client.call_async(request)

            while rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.1)
                if futur.done():
                     break

            if futur.result() is not None:
                self.get_logger().info('MoveJoint succeded')
            else:
                self.get_logger().info('MoveJoint service call failed...')

def main (args=None):
     rclpy.init(args=args)
     node = MoveHomeNode()
     node.destroy_node()
     rclpy.shutdown()

if __name__ == 'main' :
     main()







 


    







# def calculate_joint_speed(robot_position, joint_limit):
#     inner_threshold = .1 # degree
#     outer_threshold = joint_limit/2
#     max_speed = math.pi/20

#     abs_pos = abs(robot_position)
#     sign_pos = numpy.sign(robot_position)

#     if abs_pos < inner_threshold:
#         return 0
#     elif abs_pos < outer_threshold:
#         return abs_pos / outer_threshold * sign_pos * max_speed
#     else:
#         return sign_pos * max_speed 

# def go_home():
#     home_position = [0,-25,90,0,90,-90]
#     joint_limit = [360, 95, 160, 360, 135, 360]
#     inner_threshold = 0.003
#     desired_speed = Float64MultiArray()
#     desired_speed.data = [0,0,0,0,0,0]

#     is_clear = 0

#     while is_clear != 6:        
#         is_clear = 0
        
#         robot_pos = rospy.wait_for_message("/joint_states", JointState, timeout=.1)

#         if robot_pos.name[0] == "joint1":
                
#             for i in range(len(joint_limit)):
#                 joint_speed = calculate_joint_speed(home_position[i] - numpy.rad2deg(robot_pos.position[i]), joint_limit[i])
#                 desired_speed.data[i] = joint_speed

#                 if joint_speed < inner_threshold:
#                     is_clear += 1
        
#         pub_speed.publish(desired_speed)


# if __name__ == "__main__":
#     rospy.init_node("velocity_go_home_node")
    
#     global pub_speed
#     pub_speed = rospy.Publisher("/dsr_joint_velocity_controller/command", Float64MultiArray, queue_size=1)

#     go_home()

#     speed_zero = Float64MultiArray()
#     speed_zero.data = [0,0,0,0,0,0]
#     pub_speed.publish(speed_zero)

#     try:
#         print("Robot at home")
#     except rospy.ROSInterruptException:
#         pass
