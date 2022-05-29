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

gps_time = None
local_time = None
base_path = "/home/ubuntu/catkin_ws/src/ros_transfer_drone/scripts/"

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
    global ifm, gps_time, local_time
    # global drone_syn_pub
    gps_imu = drone_state_msgs_pb2.DroneState()
    # drone_syn = DroneSyn()
    # temp = ""
    # print(ros_gps_pos.header.stamp.secs,
    # ros_gps_pos.header.stamp.nsecs, type(ros_gps_pos.header.stamp.secs))
    local_time = time.time()
    gps_time = ros_gps_pos.header.stamp.secs * 1000000000 + ros_gps_pos.header.stamp.nsecs
    ts_bytes = str(gps_time).ljust(19, "0").encode()
    # print(ros_gps_pos.header.stamp.secs, ros_gps_pos.header.stamp.nsecs, gps_time)
    # gps_time_bytes = str(gps_time).ljust(19, "0").encode()
    # print(gps_time_bytes)
    # print(gps_time, int(local_time*1000000000))

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
    ifm.send_state(ts_bytes + sent_data)
    print("finish",gps_imu.gps.lon_x)

def callback_img(ros_img):
    global ifm, gps_time, local_time
    if local_time is None: return
    delta_t = time.time() - local_time
    # print(delta_t, gps_time)

    delta_t = int(delta_t* 1000000000)
    new_ts = gps_time + delta_t
    ts_bytes = str(new_ts).ljust(19, "0").encode()

    img = np.ndarray(shape=(480, 640, 3), dtype=np.dtype("uint8"), buffer=ros_img.data)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, jpeg = cv2.imencode('.jpg', img)
    data = jpeg.tobytes()
    ifm.send_img(ts_bytes + data)
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
