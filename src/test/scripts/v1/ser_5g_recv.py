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
uav_id = '0'
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
address = ('', 10001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(address)
s.listen(5)
print('Waiting for connection...')
sock, addr = s.accept()
print('Accept new connection from %s:%s...' % addr)
sock.send('Welcome!'.encode())


def talker():
    img_pub = rospy.Publisher('/ser_img_pub', Image, queue_size=1)
    odom_pub = rospy.Publisher('/ser_odom_pub', Odometry, queue_size=1)
    rospy.init_node('ser_tcp_recv', anonymous=True)

    rate = rospy.Rate(10)
    bridge = CvBridge()
    odom_msg = Odometry()
    pos = odom_msg.pose.pose.position
    ori = odom_msg.pose.pose.orientation
    while not rospy.is_shutdown():
        try:
            uav_id = int(sock.recv(1).decode())
            if uav_id == 'e':
                sock.close()
                print('The task of %s:%s has been finished.' % addr)
                break
            t_ms = int(sock.recv(8).decode())
            pos_ori = []
            for _ in range(7):
                v = int(sock.recv(8).decode()) / 1000
                pos_ori.append(v)

            data_len = int(sock.recv(7).decode())
            data = b''
            buf_len = data_len
            while data_len > 0:
                sp_data = sock.recv(buf_len)
                data += sp_data
                data_len -= len(sp_data)
            img = cv2.imdecode(np.frombuffer(data, dtype='uint8'), cv2.IMREAD_COLOR)
        except:
            break
        odom_msg.header.stamp = rospy.Time.from_sec(t_ms)
        pos.x, pos.y, pos.z = pos_ori[:3]
        ori.x, ori.y, ori.z, ori.w = pos_ori[3:]
        img_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        odom_pub.publish(odom_msg)
        print('uav_id:%s, timestamp:%s, img_shape:%s, pos:%s, ori:%s' % (uav_id, t_ms, img.shape, pos_ori[:3], pos_ori[3:]))
        cv2.imshow('video' + str(uav_id), img)
        cv2.waitKey(1)
        if cv2.waitKey(50) & 0xFF == ord(str(uav_id)):
            sock.close()
            print('The task of %s:%s has been finished.' % addr)
            break
        rate.sleep()



if __name__ == '__main__':
    talker()
