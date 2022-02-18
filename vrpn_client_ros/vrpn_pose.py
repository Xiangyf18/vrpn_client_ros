import rclpy
from rclpy.node import Node
from rclpy.publisher import Publisher


from geometry_msgs.msg import PoseStamped, TwistStamped
from geometry_msgs.msg import Twist

import time
import math
import threading

from functools import partial


class VrpnPose(Node):
    def __init__(self):
        super().__init__('VrpnPose')
        self.transfer = {}
        # TODO: in ros2 ,the arg for 'rclpy.spin' is the whole node !

        self.loop_thread = threading.Thread(target=self.main_task)
        self.loop_thread.setDaemon(True)
        self.loop_thread.start()

    def main_task(self):
        prefix = 'vrpn_client_node'
        postfix = 'pose'
        while rclpy.ok():
            topic_list = self.get_topic_names_and_types()
            for topic in topic_list:
                vrpn_topic_name: str = topic[0]
                vrpn_topic_split = vrpn_topic_name.split('/')
                if vrpn_topic_split[1] == prefix and vrpn_topic_split[-1] == postfix:
                    car_id = vrpn_topic_split[2]

                    if car_id not in self.transfer.keys():
                        sub = self.create_subscription(PoseStamped, vrpn_topic_name,
                                                       partial(self.transfer_callback,
                                                               args=(car_id,)),
                                                       qos_profile=rclpy.qos.qos_profile_sensor_data)
                        pub = self.create_publisher(TwistStamped, '/'+car_id+'/pose')
                        self.transfer[car_id] = {'sub': sub, 'pub': pub}
            print(self.transfer)
            time.sleep(1)

    def transfer_callback(self, msg: PoseStamped, args):
        car_id = args[0]
        qx = msg.pose.orientation.x
        qy = msg.pose.orientation.y
        qw = msg.pose.orientation.w
        qz = msg.pose.orientation.z
        roll = math.atan2(2*(qw*qx+qy*qz), 1-2*(qx*qx+qy*qy))
        pitch = math.asin(2*(qw*qy-qz*qx))
        yaw = math.atan2(2*(qw*qz+qx*qy), 1-2*(qz*qz+qy*qy))

        twist = TwistStamped()
        twist.header = msg.header
        twist.twist.linear.x = msg.pose.position.x
        twist.twist.linear.y = msg.pose.position.y
        twist.twist.linear.z = msg.pose.position.z
        twist.twist.angular.x = roll
        twist.twist.angular.y = pitch
        twist.twist.angular.z = yaw
        '''
        pose_list = []
        time_stamp = twist.header.stamp.secs + twist.header.stamp.nsecs/(1e9)
        pose_list.append(time_stamp)
        pose_list.append(twist.twist.linear.x)
        pose_list.append(twist.twist.linear.y)
        pose_list.append(twist.twist.linear.z)
        pose_list.append(twist.twist.angular.z)
        filename = "/home/ubuntu/project/NICS_MultiRobot_Platform/src/vrpn_client_ros/"+car_id+"pose.txt"
        with open(filename, "a") as f:
           f.write(str(pose_list))
        f.close()
        '''
        pub: Publisher = self.transfer[car_id]['pub']
        pub.publish(twist)
