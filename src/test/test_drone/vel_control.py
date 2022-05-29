#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from mavros_msgs.msg import PositionTarget, State, HomePosition

mavros_state = State()
# armServer = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
setModeServer = rospy.ServiceProxy('/mavros/set_mode', SetMode)
drone_vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped',Twist, queue_size=10)

def mavros_state_callback(msg):
	global mavros_state
	mavros_state = msg

def drone_test_publisher():
	# ROS节点初始化
    rospy.init_node('drone_test', anonymous=True)
    rospy.Subscriber("/mavros/state", State, mavros_state_callback) 
    
    
    rate = rospy.Rate(20) 
    drone_vel = Twist()
    print("Initialized")

    drone_vel.linear.x = 0###take off
    drone_vel.linear.y = 0
    drone_vel.linear.z = 2#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1
    # drone_vel.angular[1] = 0.1
    # drone_vel.angular[2] = 0.1
    
    drone_vel_pub.publish(drone_vel)
    print("take off")
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue
    
    drone_vel.linear.x = 0
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.
    
    drone_vel_pub.publish(drone_vel)
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(1.0):
        continue

    drone_vel.linear.x = 0###fly to north
    drone_vel.linear.y = 1
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1    
    drone_vel_pub.publish(drone_vel)
    print("fly to north")
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue


    drone_vel.linear.x = 0
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.
    
    drone_vel_pub.publish(drone_vel)
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(1.0):
        continue

    drone_vel.linear.x = -1###fly to west
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1    
    drone_vel_pub.publish(drone_vel)
    print("fly to north")
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue

    drone_vel.linear.x = 0
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.
    
    drone_vel_pub.publish(drone_vel)
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(1.0):
        continue

    drone_vel.linear.x = 0###fly to south
    drone_vel.linear.y = -1
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1    
    drone_vel_pub.publish(drone_vel)
    print("fly to south")
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue

    drone_vel.linear.x = 0
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.
    
    drone_vel_pub.publish(drone_vel)
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(1.0):
        continue

    drone_vel.linear.x = 1###fly to east
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.1    
    drone_vel_pub.publish(drone_vel)
    print("fly to east")
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue

    drone_vel.linear.x = 0
    drone_vel.linear.y = 0
    drone_vel.linear.z = 0#[0.05,0.05,0.05]
    drone_vel.angular.z = 0# drone_vel.angular[0] = 0.
    
    drone_vel_pub.publish(drone_vel)
    flight_time = rospy.Time.now()
    while (rospy.Time.now()-flight_time)<=rospy.Duration(2.0):
        continue
    
    if mavros_state.mode != "AUTO.LAND":
        setModeServer(custom_mode="AUTO.LAND")
        drone_vel_pub.publish(drone_vel)
        print("wait offboard")




if __name__ == '__main__':
    try:
        drone_test_publisher()
    except rospy.ROSInterruptException:
        pass
