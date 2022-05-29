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


global img
global pos_ori
img_size = (720, 1280, 3)  # 720p
# img_size = (1080, 1920, 3)  # 1080p
# img_size = (2160, 3840, 3)  # 4K
uav_id = '0'
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
address = ('127.0.0.1', 10001)
# address = ('1.13.1.128', 10001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(10).decode())
pub = rospy.Publisher('/obj_pos_tr', Twist, queue_size=1)

def img_callback(imgmsg):
    global img
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    # tcp_link()



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
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/img_tr", Image, img_callback)
    # rospy.Subscriber("/odom_tr", Odometry, odom_callback)
    rospy.Subscriber("/camera/fisheye1/image_raw", Image, img_callback)
    rospy.Subscriber("/camera/odom/sample", Odometry, odom_callback)
    # rospy.spin()

    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        try:
            tcp_link()
        except:
            rospy.signal_shutdown('TCP interruption')
        obj_pos_msg = Twist()
        obj_pos_msg.linear.x = obj_pos[0]
        obj_pos_msg.linear.y = obj_pos[1]
        obj_pos_msg.linear.z = obj_pos[2]
        pub.publish(obj_pos_msg)
        rospy.loginfo("Publsh obj_pos message[%f, %f, %f]",
                      obj_pos_msg.linear.x, obj_pos_msg.linear.y, obj_pos_msg.linear.z)
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
    s.sendall(data)
    # print(len(data))
    obj_pos[0] = int(s.recv(8).decode()) / 1000.
    obj_pos[1] = int(s.recv(8).decode()) / 1000.
    obj_pos[2] = int(s.recv(8).decode()) / 1000.

    # obj_pos = Twist()
    # obj_pos.linear.x = int(s.recv(8).decode()) / 1000.
    # obj_pos.linear.y = int(s.recv(8).decode()) / 1000.
    # obj_pos.linear.z = int(s.recv(8).decode()) / 1000.
    # pub.publish(obj_pos)
    # rospy.loginfo("Publsh obj_pos message[%f, %f, %f]",
    #               obj_pos.linear.x, obj_pos.linear.y, obj_pos.linear.z)


if __name__ == '__main__':
    img = np.array(img_size, np.uint8)
    pos_ori = [0.] * 7
    obj_pos = [0.] * 3
    listener()
