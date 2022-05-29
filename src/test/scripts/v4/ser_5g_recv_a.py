#!/usr/bin/env python
import numpy as np
import rospy
import socket
from sensor_msgs.msg import Image
import cv2
import time
from cv_bridge import CvBridge
from nav_msgs.msg  import Odometry
from geometry_msgs.msg import Twist


img_size = (720, 1280, 3)  # 720p
# img_size = (1080, 1920, 3)  # 1080p
# img_size = (2160, 3840, 3)  # 4K

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 10001))
s.listen(5)
print('Waiting for connection...')
sock, address = s.accept()
print('Accept new connection from %s:%s...' % address)
# sock.send('Welcome!'.encode())
uav_id = sock.recv(2).decode()

def talker():
    col_img_pub = rospy.Publisher('/ser_col_img_pub_' + uav_id, Image, queue_size=1)
    dep_img_pub = rospy.Publisher('/ser_dep_img_pub_' + uav_id, Image, queue_size=1)
    odom_pub = rospy.Publisher('/ser_odom_pub_' + uav_id, Odometry, queue_size=1)
    rospy.init_node('ser_tcp_recv', anonymous=True)

    rate = rospy.Rate(10)
    bridge = CvBridge()
    odom_msg = Odometry()
    pos = odom_msg.pose.pose.position
    ori = odom_msg.pose.pose.orientation
    while not rospy.is_shutdown():
        len1 = int(sock.recv(7).decode())
        len2 = int(sock.recv(7).decode())
        len3 = int(sock.recv(7).decode())
        totol_len = len1 + len2 + len3 + 89
        data = b''
        cnt_len = totol_len
        while cnt_len > 0:
            sp_data = sock.recv(totol_len)
            data += sp_data
            cnt_len -= len(sp_data)
        sock.send('ok'.encode())
        if len(data) != totol_len:
            continue

        t_s = int(data[:10].decode())
        t_ns = int(data[10:19].decode())
        pos_ori = []
        for i in range(7):
            v = float(data[19 + 10 * i:19 + 10 * (i + 1)].decode())
            pos_ori.append(v)
        col_img = cv2.imdecode(np.frombuffer(data[89:89 + len1], dtype='uint8'), cv2.IMREAD_COLOR)
        dep_img_1 = cv2.imdecode(np.frombuffer(data[89 + len1:89 + len1 + len2], dtype='uint8'), cv2.IMREAD_ANYDEPTH)
        dep_img_2 = cv2.imdecode(np.frombuffer(data[89 + len1 + len2:], dtype='uint8'), cv2.IMREAD_ANYDEPTH)
        dep_img = (np.uint16(dep_img_2) << 8) + dep_img_1

        odom_msg.header.stamp.secs, odom_msg.header.stamp.nsecs = t_s, t_ns
        pos.x, pos.y, pos.z = pos_ori[:3]
        ori.x, ori.y, ori.z, ori.w = pos_ori[3:]
        col_img_msg = bridge.cv2_to_imgmsg(col_img, "bgr8")
        col_img_msg.header.stamp.secs, col_img_msg.header.stamp.nsecs = t_s, t_ns
        dep_img_msg = bridge.cv2_to_imgmsg(dep_img, "16UC1")
        dep_img_msg.header.stamp.secs, dep_img_msg.header.stamp.nsecs = t_s, t_ns

        col_img_pub.publish(col_img_msg)
        dep_img_pub.publish(dep_img_msg)
        odom_pub.publish(odom_msg)
        print('uav_id:%s, timestamp:%s, col_img_shape:%s, dep_img_shape:%s, pos:%s, ori:%s'
              % (uav_id, t_s + t_ns, col_img.shape, dep_img.shape, pos_ori[:3], pos_ori[3:]))
        cv2.imshow('col_img' + str(uav_id), col_img)
        dep_img_vis = cv2.applyColorMap(cv2.convertScaleAbs(dep_img, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow('dep_img' + str(uav_id), dep_img_vis)
        cv2.waitKey(1)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            sock.close()
            print('The task of %s:%s has been finished.' % address)
            break
        rate.sleep()



if __name__ == '__main__':
    talker()
