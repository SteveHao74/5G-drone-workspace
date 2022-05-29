#!/usr/bin/env python
import numpy as np
import rospy
import socket
from sensor_msgs.msg import Image
import cv2
import time
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose


address = ('127.0.0.1', 10002)
# address = ('10.10.129.198', 10002)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(10).decode())


def talker():
    rospy.init_node('tcp_recv', anonymous=True)
    pub = rospy.Publisher('/obj_pos_pub', Odometry, queue_size=1)
    rate = rospy.Rate(10)
    obj_pos_msg = Odometry()
    pos = obj_pos_msg.pose.pose.position
    ori = obj_pos_msg.pose.pose.orientation
    vet = obj_pos_msg.twist.twist.linear
    
    while not rospy.is_shutdown():
        obj_pos = []
        for _ in range(10):
            v = float(s.recv(10).decode())
            obj_pos.append(v)
        s.send('ok'.encode())
        pos.x, pos.y, pos.z = obj_pos[:3]
        ori.x, ori.y, ori.z, ori.w = obj_pos[3:7]
        vet.x, vet.y, vet.z = obj_pos[7:]
        
        pub.publish(obj_pos_msg)
        rospy.loginfo("Publsh obj_pos message %s", obj_pos)
        rate.sleep()


if __name__ == '__main__':
    talker()
