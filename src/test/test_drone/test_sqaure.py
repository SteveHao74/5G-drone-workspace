#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.msg import PositionTarget, State, HomePosition
from sensor_msgs.msg import Image, Imu, NavSatFix
mavros_state = State()
setModeServer = rospy.ServiceProxy('/mavros/set_mode', SetMode)

def mavros_state_callback(msg):
	global mavros_state
	mavros_state = msg

def drone_test_publisher():
	# ROS节点初始化
    rospy.init_node('drone_test', anonymous=True)
    global target_pos_pub
    drone_vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped',Twist, queue_size=10)
    rospy.Subscriber("/mavros/state", State, mavros_state_callback)
    
    rate = rospy.Rate(20) 
    drone_vel = Twist()
    wait_time = 6.0
    run_time = 6.0
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
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time+run_time):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0.5
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("north")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*2+run_time):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0           
            print("pause")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*2+run_time*2):
            drone_vel.linear.x = -0.5
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("west")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*3+run_time*2):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0 
            print("pause")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*3+run_time*3):
            drone_vel.linear.x = 0
            drone_vel.linear.y = -0.5
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("south")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*4+run_time*3):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("pause")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*4+run_time*4):
            drone_vel.linear.x = 0.5
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
            print("east")
        elif (rospy.Time.now()-flight_time)<=rospy.Duration(wait_time+pause_time*5+run_time*4):
            drone_vel.linear.x = 0
            drone_vel.linear.y = 0
            drone_vel.linear.z = 0#[0.05,0.05,0.05]
            drone_vel.angular.z = 0
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

