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
import message_filters

# global img
# global pos_ori

img_size = (720, 1280, 3)  # 720p
# img_size = (1080, 1920, 3)  # 1080p
# img_size = (2160, 3840, 3)  # 4K
uav_id = '01'
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
address = ('127.0.0.1', 10001)
# address = ('1.13.1.128', 10001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
# print(s.recv(10).decode())
s.sendall(uav_id.encode())




def listener():
    rospy.init_node('tcp_send', anonymous=True)
    # img_sub = message_filters.Subscriber("/img_tr", Image)
    # odom_sub = message_filters.Subscriber("/odom_tr", Odometry)
    img_sub = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
    odom_sub = message_filters.Subscriber("/camera/odom/sample", Odometry)

    ts = message_filters.ApproximateTimeSynchronizer([img_sub, odom_sub], 10, 0.1, allow_headerless=True)
    ts.registerCallback(tcp_link)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()




def tcp_link(img_msg, odom_msg):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    odom_pos = odom_msg.pose.pose.position
    odom_ori = odom_msg.pose.pose.orientation
    rospy.loginfo("Subscribe odom message [%f, %f, %f, %f, %f, %f, %f, %s]",
                  odom_pos.x, odom_pos.y, odom_pos.z,
                  odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w, img.shape)
    pos_ori = [odom_pos.x, odom_pos.y, odom_pos.z,
               odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w]

    t = rospy.Time.now()
    data = str(t.secs).encode() + str(t.nsecs).zfill(9).encode()
    for v in pos_ori:
        val = str(v)[:10].ljust(10, '0')
        data += val.encode()
    # img = cv2.resize(img, (img_size[1], img_size[0]), interpolation=cv2.INTER_AREA)
    ret, jpg = cv2.imencode('.jpg', img, encode_param)
    jpg_len = str(len(jpg)).zfill(7)
    data += jpg_len.encode()
    data += jpg.tobytes()
    s.sendall(data)
    time.sleep(0.1)



if __name__ == '__main__':
    listener()
