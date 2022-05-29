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
    img_pub = rospy.Publisher('/ser_img_pub_' + uav_id, Image, queue_size=1)
    odom_pub = rospy.Publisher('/ser_odom_pub_' + uav_id, Odometry, queue_size=1)
    rospy.init_node('ser_tcp_recv', anonymous=True)

    rate = rospy.Rate(10)
    bridge = CvBridge()
    odom_msg = Odometry()
    pos = odom_msg.pose.pose.position
    ori = odom_msg.pose.pose.orientation
    while not rospy.is_shutdown():
        t_s = int(sock.recv(10).decode())
        t_ns = int(sock.recv(9).decode())
        pos_ori = []
        for _ in range(7):
            v = float(sock.recv(10).decode())
            pos_ori.append(v)
        img_len = int(sock.recv(7).decode())
        data = b''
        buf_len = img_len
        while img_len > 0:
            sp_data = sock.recv(buf_len)
            data += sp_data
            img_len -= len(sp_data)
        img = cv2.imdecode(np.frombuffer(data, dtype='uint8'), cv2.IMREAD_COLOR)

        odom_msg.header.stamp.secs, odom_msg.header.stamp.nsecs = t_s, t_ns
        pos.x, pos.y, pos.z = pos_ori[:3]
        ori.x, ori.y, ori.z, ori.w = pos_ori[3:]
        img_msg = bridge.cv2_to_imgmsg(img, "bgr8")
        img_msg.header.stamp.secs, img_msg.header.stamp.nsecs = t_s, t_ns

        img_pub.publish(img_msg)
        odom_pub.publish(odom_msg)
        print('uav_id:%s, timestamp:%s, img_shape:%s, pos:%s, ori:%s' % (uav_id, t_s + t_ns, img.shape, pos_ori[:3], pos_ori[3:]))
        cv2.imshow('video' + str(uav_id), img)
        cv2.waitKey(1)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            sock.close()
            print('The task of %s:%s has been finished.' % address)
            break
        rate.sleep()



if __name__ == '__main__':
    talker()
