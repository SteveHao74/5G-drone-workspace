from time import sleep
import cv2
import math
import numpy as np
import message_filters
import rospy
from std_msgs.msg import Header
from geometry_msgs.msg import Twist, Vector3 ,PoseStamped
from sensor_msgs.msg import Image, Imu, NavSatFix
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

def gps2xy(longtitude, latitude):
    L = 6381372*math.pi*2
    W = L
    H = L/2
    mill = 2.3
    x = longtitude*math.pi/180
    y = latitude*math.pi/180
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    return x, y

def callback_syn(ros_gps,ros_imu):
    global msg_pub
    msg = PoseStamped()
    msg.header = Header()
    msg.header.frame_id = 'map'
    msg.pose.orientation.x = ros_imu.orientation.x
    msg.pose.orientation.y = ros_imu.orientation.y
    msg.pose.orientation.z = ros_imu.orientation.z
    msg.pose.orientation.w = ros_imu.orientation.w
    
    x,y=gps2xy(ros_gps.longitude,ros_gps.latitude)
    
    msg.pose.position.x = x - 33425780
    msg.pose.position.y = y - 7650172
    msg.pose.position.z = ros_gps.altitude
    msg_pub.publish(msg)
    print("finish")



if __name__ == '__main__':
    rospy.init_node('5g-transfer', anonymous=True)
    global msg_pub 
    msg_pub = rospy.Publisher('/visual_pose_4', PoseStamped, queue_size=0)
    # rospy.Subscriber('/camera/color/image_raw', Image, callback_img)
    # rospy.Subscriber('/mavros/altitude', Altitude, callback_altitude)
    # rospy.Subscriber('/mavros/battery', BatteryState, callback_battery)
    # rospy.Subscriber('/mavros/global_position/raw/gps_vel', TwistStamped, callback_gps_vel)
    sub_gps = message_filters.Subscriber('/mavros/global_position/global', NavSatFix)
    sub_imu = message_filters.Subscriber('/mavros/imu/data', Imu)
    sync_listener = message_filters.ApproximateTimeSynchronizer([sub_gps,sub_imu], 10, 1)#, allow_headerless=True
    sync_listener.registerCallback(callback_syn)

    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        rate.sleep()

