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

img = None
pos_ori = []
address = ('', 10002)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(5)
print('Waiting for connection...')
sock, addr = s.accept()
print('Accept new connection from %s:%s...' % addr)
sock.send('Welcome!'.encode())


def get_obj_pos(im, po):
    # res = [1023.23, -342.39, 101.01]
    res = po[:3]
    return res


def img_callback(imgmsg):
    global img
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")


def odom_callback(odom_msg):
    global pos_ori
    odom_pos = odom_msg.pose.pose.position
    odom_ori = odom_msg.pose.pose.orientation
    # rospy.loginfo("Subscribe odom message [%1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f]",
    #               odom_pos.x, odom_pos.y, odom_pos.z,
    #               odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w)
    pos_ori = [odom_pos.x, odom_pos.y, odom_pos.z,
               odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w]


def listener():
    rospy.init_node('ser_tcp_send', anonymous=True)
    rospy.Subscriber("/ser_img_pub", Image, img_callback)
    rospy.Subscriber("/ser_odom_pub", Odometry, odom_callback)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        obj_pos = get_obj_pos(img, pos_ori)
        try:
            tcp_link(obj_pos)
            rospy.loginfo("Send object position: %s", obj_pos)
        except:
            sock.close()
            break
        rate.sleep()


def tcp_link(obj_pos):
    data = b''
    for v in obj_pos:
        if v < 0:
            val = '-' + str(int(-v * 1000)).zfill(7)
        else:
            val = str(int(v * 1000)).zfill(8)
        data += val.encode()
    sock.sendall(data)



if __name__ == '__main__':
    listener()
