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
from turbojpeg import TurboJPEG
import lz4framed

# global img
# global pos_ori

img_size = (720, 1280, 3)  # 720p
# img_size = (1080, 1920, 3)  # 1080p
# img_size = (2160, 3840, 3)  # 4K
uav_id = '01'
address = ('127.0.0.1', 10001)
# address = ('10.10.129.198', 10001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.send(uav_id.encode())
bridge = CvBridge()
jpeg = TurboJPEG()


def listener():
    rospy.init_node('tcp_send', anonymous=True)
    # img_sub = message_filters.Subscriber("/img_tr", Image)
    odom_sub = message_filters.Subscriber("/odom_tr", Odometry)
    # img_sub = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
    # odom_sub = message_filters.Subscriber("/camera/odom/sample", Odometry)
    col_img_sub = message_filters.Subscriber("/camera/color/image_raw", Image)
    dep_img_sub = message_filters.Subscriber("/camera/depth/image_rect_raw", Image)
    # dep_img_sub = message_filters.Subscriber("/camera/aligned_depth_to_color/image_raw", Image)

    ts = message_filters.ApproximateTimeSynchronizer([odom_sub, col_img_sub, dep_img_sub], 10, 0.1, allow_headerless=True)
    ts.registerCallback(tcp_link)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()




def tcp_link(odom_msg, col_img_msg, dep_img_msg):

    col_img = bridge.imgmsg_to_cv2(col_img_msg, "bgr8")
    dep_img = bridge.imgmsg_to_cv2(dep_img_msg, '16UC1')

    odom_pos = odom_msg.pose.pose.position
    odom_ori = odom_msg.pose.pose.orientation
    rospy.loginfo("Subscribe odom message [%f, %f, %f, %f, %f, %f, %f]",
                  odom_pos.x, odom_pos.y, odom_pos.z,
                  odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w)
    pos_ori = [odom_pos.x, odom_pos.y, odom_pos.z,
               odom_ori.x, odom_ori.y, odom_ori.z, odom_ori.w]

    data = b''
    t = rospy.Time.now()
    data += str(t.secs).encode() + str(t.nsecs).zfill(9).encode()
    for v in pos_ori:
        val = str(v)[:10].ljust(10, '0')
        data += val.encode()
    # img = cv2.resize(img, (img_size[1], img_size[0]), interpolation=cv2.INTER_AREA)
    col_img_jpg = jpeg.encode(col_img, quality=80)
    dep_img_lz4 = lz4framed.compress(dep_img.tobytes())
    len1 = str(len(col_img_jpg)).zfill(7)
    len2 = str(len(dep_img_lz4)).zfill(7)

    data += len1.encode()
    data += len2.encode()
    data += col_img_jpg
    data += dep_img_lz4
    s.sendall(data)
    s.recv(2)
    # dep_img_vis = cv2.applyColorMap(cv2.convertScaleAbs(dep_img, alpha=0.03), cv2.COLORMAP_JET)
    # cv2.imshow('dep_img', dep_img_vis)
    # cv2.waitKey(10)



if __name__ == '__main__':
    listener()
