#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import message_filters
import rospy
from sensor_msgs.msg import Image, Imu, NavSatFix
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from proto.python_out import drone_state_msgs_pb2

from informer import Informer
cnt = 0
def parse_cmd(message, robot_id):
    print("Get cmd:", message)

class Client(Informer):
    def send_img(self, message):
        self.send(message, 'img')

    def send_state(self, message):
        self.send(message, 'state')
    
    def cmd_recv(self):
        self.recv('cmd', parse_cmd)

def callback_syn(ros_gps_pos,ros_gps_vel,ros_imu,ros_local_vel):
    global ifm
    print("1234")
    # global drone_syn_pub
    gps_imu = drone_state_msgs_pb2.DroneState()
    # drone_syn = DroneSyn()
    temp = ""
    gps_imu.gps.lon_x = ros_gps_pos.longitude
    gps_imu.gps.lat_y = ros_gps_pos.latitude
    gps_imu.gps.alt_z = ros_gps_pos.altitude

    gps_imu.gps.vx = ros_gps_vel.twist.linear.x
    gps_imu.gps.vy = ros_gps_vel.twist.linear.y
    gps_imu.gps.vz = ros_local_vel.twist.twist.linear.z#ros_gps_vel.twist.linear.z

    gps_imu.imu.quan_x = ros_imu.orientation.x
    gps_imu.imu.quan_y = ros_imu.orientation.y
    gps_imu.imu.quan_z = ros_imu.orientation.z
    gps_imu.imu.quan_w = ros_imu.orientation.w
    
    gps_imu.imu.w_x = ros_imu.angular_velocity.x
    gps_imu.imu.w_y = ros_imu.angular_velocity.y
    gps_imu.imu.w_z = ros_imu.angular_velocity.z
    sent_data = gps_imu.SerializeToString()
    # drone_syn_pub.publish(drone_syn)
    ifm.send_state(sent_data)
    print("finish",ros_imu.angular_velocity.x)

def callback_img(ros_img):
    global ifm,cnt
    cnt += 1
    if cnt%3 == 0:
        img = np.ndarray(shape=(480, 640, 3), dtype=np.dtype("uint8"), buffer=ros_img.data)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, jpeg = cv2.imencode('.jpg', img)
        data = jpeg.tobytes()
        ifm.send_img(data)
    # cv2.imshow('img', img)
    # cv2.waitKey(2)

if __name__ == '__main__':
    ifm = Client(config = 'config.yaml')
    # import pdb;pdb.set_trace()
    rospy.init_node('drone_5g_transfer', anonymous=True)
    # drone_syn_pub = rospy.Publisher('/drone_1', DroneSyn, queue_size=10)
    sub_camera = message_filters.Subscriber('/camera/color/image_raw', Image)
    sub_gps = message_filters.Subscriber('/mavros/global_position/global', NavSatFix)
    sub_gps_vel = message_filters.Subscriber('/mavros/global_position/raw/gps_vel', TwistStamped)
    sub_local_vel = message_filters.Subscriber('/mavros/global_position/local', Odometry)
    sub_imu = message_filters.Subscriber('/mavros/imu/data', Imu)
    sync_listener = message_filters.ApproximateTimeSynchronizer([sub_gps,sub_gps_vel,sub_imu,sub_local_vel], 10, 1)#, allow_headerless=True
    sync_listener.registerCallback(callback_syn)
    rospy.Subscriber('/camera/color/image_raw', Image, callback_img)

    # rospy.spin()
    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        rate.sleep()
