#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.msg import PositionTarget, State, HomePosition
from sensor_msgs.msg import Image, Imu, NavSatFix
import numpy as np
mavros_state = State()
setModeServer = rospy.ServiceProxy('/mavros/set_mode', SetMode)
mavros_altitude = 0
########
set_mavros_altitude = 0
init_mavros_altitude = 0
kp_z = 1

def mavros_state_callback(msg):
	global mavros_state
	mavros_state = msg

def mavros_altitude_callback(ros_gps_pos):
	global mavros_altitude
	mavros_altitude = ros_gps_pos.altitude
    #     _ = ros_gps_pos.latitude
    #     _ = ros_gps_pos.longtitude

def drone_test_publisher():
	# ROS节点初始化
    rospy.init_node('drone_test', anonymous=True)
    global target_pos_pub
    rospy.Subscriber("/mavros/global_position/global", NavSatFix, mavros_altitude_callback)
    drone_vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped',Twist, queue_size=10)
    rospy.Subscriber("/mavros/state", State, mavros_state_callback)
    rate = rospy.Rate(10) 
    drone_vel = Twist()
    wait_time = 6.0
    run_time = 10.0
    pause_time = 1.0
    flight_time = rospy.Time.now()
    while not rospy.is_shutdown():
        if (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 2#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("take off")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1
            print("pause")
            init_mavros_altitude = mavros_altitude
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time+run_time):
            wz = 0.3
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = wz
            print("rotate")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*2+run_time):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1
            print("pause")
        else:
            if mavros_state.mode != "AUTO.LAND":
                setModeServer(custom_mode="AUTO.LAND")
                drone_vel_pub.publish(drone_vel)
                print("landing")
                break
        # 初始化learning_topic::Person类型的消息
        # drone_vel.angular[1] = 0.1
        # drone_vel.angular[2] = 0.1
        drone_vel_pub.publish(drone_vel)
        print("flight_time:",rospy.Time.now()-flight_time)
        # 按照循环频率延时
        rate.sleep()


if __name__ == '__main__':
    try:
        drone_test_publisher()
    except rospy.ROSInterruptException:
        pass

