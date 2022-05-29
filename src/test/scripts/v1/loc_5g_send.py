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

# global img
# global pos_ori
img = None
pos_ori = []
img_size = (720, 1280, 3)  # 720p
# img_size = (1080, 1920, 3)  # 1080p
# img_size = (2160, 3840, 3)  # 4K
uav_id = '0'
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
address = ('127.0.0.1', 10001)
# address = ('1.13.1.128', 10001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(10).decode())


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
    rospy.init_node('tcp_send', anonymous=True)
    # rospy.Subscriber("/img_tr", Image, img_callback)
    # rospy.Subscriber("/odom_tr", Odometry, odom_callback)
    rospy.Subscriber("/camera/fisheye1/image_raw", Image, img_callback)
    rospy.Subscriber("/camera/odom/sample", Odometry, odom_callback)
    # rospy.spin()

    rate = rospy.Rate(10)
    cnt = 0
    while not rospy.is_shutdown():
        if img is not None and pos_ori:
            if tcp_link():
                cnt += 1
                rospy.loginfo("Send data num [%d]", cnt)
            else:
                break
        rate.sleep()


def tcp_link():
    # img = cv2.resize(img, (img_size[1], img_size[0]), interpolation=cv2.INTER_AREA)
    ret, jpg = cv2.imencode('.jpg', img, encode_param)
    jpg_len = str(len(jpg)).zfill(7)
    t_ms = str(int(time.time() * 1000))[-8:]
    data = (uav_id + t_ms).encode()
    for v in pos_ori:
        if v < 0:
            val = '-' + str(int(-v * 1000)).zfill(7)
        else:
            val = str(int(v * 1000)).zfill(8)
        data += val.encode()
    data += jpg_len.encode()
    data += jpg.tobytes()
    # noinspection PyBroadException
    try:
        s.sendall(data)
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    listener()
