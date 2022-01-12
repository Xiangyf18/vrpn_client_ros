#!/usr/bin/python3

from vrpn_client_ros.vrpn_pose import VrpnPose
import rclpy


def main():
    rclpy.init()
    client = VrpnPose()
    rclpy.spin(client)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
