#!/usr/bin/env python
import numpy as np
import rospy
import socket
from sensor_msgs.msg import Image, CompressedImage, NavSatFix
import cv2
import time
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseStamped
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
# address = ('1.13.6.145', 8008)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.send(uav_id.encode())
bridge = CvBridge()
jpeg = TurboJPEG()
pre_t = time.time()


def listener():
    rospy.init_node('tcp_send', anonymous=True)
    # img_sub = message_filters.Subscriber("/img_tr", Image)
    # odom_sub = message_filters.Subscriber("/odom_tr", Odometry)
    # img_sub = message_filters.Subscriber("/camera/fisheye1/image_raw", Image)
    # odom_sub = message_filters.Subscriber("/camera/odom/sample", Odometry)
    # col_img_sub = message_filters.Subscriber("/camera/color/image_raw", Image)
    col_img_sub = message_filters.Subscriber("/camera/color/image_raw/compressed", CompressedImage)
    dep_img_sub = message_filters.Subscriber("/camera/depth/image_rect_raw", Image)
    # dep_img_sub = message_filters.Subscriber("/camera/aligned_depth_to_color/image_raw", Image)

    gps_sub = message_filters.Subscriber("/mavros/global_position/global", NavSatFix)
    pos_sub = message_filters.Subscriber("/mavros/local_position/pose", PoseStamped)
    
    #v_sub = message_filters.Subscriber("/mavros/global_position/raw/gps_vel", TwistStamped)

    # ts = message_filters.ApproximateTimeSynchronizer([col_img_sub, dep_img_sub], 10, 0.1, allow_headerless=True)
    ts = message_filters.ApproximateTimeSynchronizer([col_img_sub, dep_img_sub, gps_sub, pos_sub], 10, 0.1, allow_headerless=True)
    ts.registerCallback(tcp_link)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def tcp_link(col_img_msg, dep_img_msg, gps_msg, pos_msg):
    # col_img = bridge.imgmsg_to_cv2(col_img_msg, "bgr8")
    # dep_img = bridge.imgmsg_to_cv2(dep_img_msg, '16UC1')

    latitude, longitude, altitude = gps_msg.latitude, gps_msg.longitude, gps_msg.altitude
    
    loc_pos = pos_msg.pose.position
    loc_ori = pos_msg.pose.orientation
    
    #v_x = v_msg.twist.linear.x
    #v_y = v_msg.twist.linear.y
    #v_z = v_msg.twist.linear.z
    
    
    pos_ori = [latitude, longitude, altitude,
               loc_pos.x, loc_pos.y, loc_pos.z,
               loc_ori.x, loc_ori.y, loc_ori.z, loc_ori.w]
    # print('global_gps: %s, local_position: %s, local_orientation: %s' % (pos_ori[:3], pos_ori[3:6], pos_ori[6:]))

    data = b''
    t = rospy.Time.now()
    data += str(t.secs).encode() + str(t.nsecs).zfill(9).encode()
    for v in pos_ori:
        val = str(v)[:10].ljust(10, '0')
        data += val.encode()
    # img = cv2.resize(img, (img_size[1], img_size[0]), interpolation=cv2.INTER_AREA)
    
    #data += str(v_x).ljust(10,'0').encode()
    #data += str(v_y).ljust(10,'0').encode()
    #data += str(v_z).ljust(10,'0').encode()
    
    col_img_jpg = col_img_msg.data
    dep_img_lz4 = lz4framed.compress(dep_img_msg.data)
    len1 = str(len(col_img_jpg)).zfill(7)
    len2 = str(len(dep_img_lz4)).zfill(7)

    data += len1.encode()
    data += len2.encode()
    data += col_img_jpg
    data += dep_img_lz4
    s.sendall(data)
    s.recv(2)
    global pre_t
    cur_t = time.time()
    print('data_size: %.4fMbits, depth_compress_ratio: %.2f, time_interval: %.2fms' % (len(data) * 8 / 1e6, len(dep_img_msg.data) / len(dep_img_lz4), (cur_t - pre_t) * 1e3))
    pre_t = cur_t



if __name__ == '__main__':
    listener()
