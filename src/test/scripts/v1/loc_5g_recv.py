#!/usr/bin/env python
import numpy as np
import rospy
import socket
from sensor_msgs.msg import Image
import cv2
import time
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


address = ('127.0.0.1', 10002)
# address = ('1.13.1.128', 10002)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(10).decode())


def talker():
    rospy.init_node('tcp_recv', anonymous=True)
    pub = rospy.Publisher('/obj_pos_pub', Twist, queue_size=1)
    rate = rospy.Rate(10)
    obj_pos_msg = Twist()
    op = obj_pos_msg.linear
    while not rospy.is_shutdown():
        try:
            obj_pos = []
            for _ in range(3):
                v = int(s.recv(8).decode()) / 1000
                obj_pos.append(v)
            op.x, op.y, op.z = obj_pos
            pub.publish(obj_pos_msg)
            rospy.loginfo("Publsh obj_pos message [%f, %f, %f]", op.x, op.y, op.z)
            rate.sleep()
        except:
            break
        rate.sleep()


if __name__ == '__main__':
    talker()
