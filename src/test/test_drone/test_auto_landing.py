#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.msg import PositionTarget, State, HomePosition
from sensor_msgs.msg import Image, Imu, NavSatFix
import numpy as np
import time 

NAME_SPACE = ""#"/iris_0"
mavros_state = State()
setModeServer = rospy.ServiceProxy(NAME_SPACE+'/mavros/set_mode', SetMode)
mavros_altitude = 0
########
set_mavros_altitude = 0

kp_z = 1.5

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
    # rospy.Subscriber(NAME_SPACE+"/mavros/global_position/global", NavSatFix, mavros_altitude_callback)
    # drone_vel_pub = rospy.Publisher(NAME_SPACE+'/mavros/setpoint_velocity/cmd_vel_unstamped',Twist, queue_size=10)
    rospy.Subscriber(NAME_SPACE+"/mavros/state", State, mavros_state_callback)
    
    rate = rospy.Rate(10) 
    drone_vel = Twist()
    wait_time = 5
    run_time = 1
    pause_time = 1.0
    flight_time = time.time()#rospy.Time.now()

    finish_landing_flag = 0

    while not rospy.is_shutdown():

        if (time.time()-flight_time)<=wait_time:#rospy.Duration(wait_time):#mavros_state.mode != "OFFBOARD":
            print("wait for landing",time.time()-flight_time)
        else:
            if finish_landing_flag==0:
                if mavros_state.mode != "AUTO.LAND":
                    setModeServer(custom_mode="AUTO.LAND")
                    # drone_vel_pub.publish(drone_vel)
                    print("during landing",time.time()-flight_time)
                
            if mavros_state.system_status == 3:
                finish_landing_flag = 1
                print("finish landing",time.time()-flight_time)
                break


        rate.sleep()

    



if __name__ == '__main__':
    try:
        drone_test_publisher()
    except rospy.ROSInterruptException:
        pass

