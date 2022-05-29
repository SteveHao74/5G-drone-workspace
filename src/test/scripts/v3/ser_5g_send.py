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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 10002))
s.listen(5)
print('Waiting for connection...')
sock, address = s.accept()
print('Accept new connection from %s:%s...' % address)
sock.send('Welcome!'.encode())


def listener():
    rospy.init_node('ser_tcp_send', anonymous=True)
    rospy.Subscriber("/odom_tr", Odometry, tcp_link)
    rospy.spin()


def tcp_link(odom_msg):
    odom_pos = odom_msg.pose.pose.position
    odom_ori = odom_msg.pose.pose.orientation
    obj_pos = [odom_pos.x, odom_pos.y, odom_pos.z,
               odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w]
    rospy.loginfo("Subscribe odom message [%f, %f, %f, %f, %f, %f, %f]",
                  odom_pos.x, odom_pos.y, odom_pos.z,
                  odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w)
    data = b''
    for v in obj_pos:
        val = str(v)[:10].ljust(10, '0')
        data += val.encode()
    sock.sendall(data)
    time.sleep(0.1)



if __name__ == '__main__':
    listener()
