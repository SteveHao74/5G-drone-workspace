#!/usr/bin/env python
# license removed for brevity
import time

import rospy
from  nav_msgs.msg  import Odometry
import random


def talker():
     pub = rospy.Publisher('/odom_tr', Odometry, queue_size=1)
     rospy.init_node('img_tr', anonymous=True)
     rate = rospy.Rate(30)
     odom_msg = Odometry()
     while not rospy.is_shutdown():
         odom_msg.header.stamp = rospy.Time.now()
         odom_msg.pose.pose.position.x = 1032.5
         odom_msg.pose.pose.position.y = -27.345
         odom_msg.pose.pose.position.z = 106.55
         odom_msg.pose.pose.orientation.x = random.random()
         odom_msg.pose.pose.orientation.y = random.random()
         odom_msg.pose.pose.orientation.z = random.random()
         odom_msg.pose.pose.orientation.w = random.random()
         odom_msg.twist.twist.linear.x = random.random()
         odom_msg.twist.twist.linear.y = random.random()
         odom_msg.twist.twist.linear.z = random.random()
         pub.publish(odom_msg)
         rospy.loginfo("Publsh odom message [%1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f]",
                       odom_msg.pose.pose.position.x, odom_msg.pose.pose.position.y, odom_msg.pose.pose.position.z,
                       odom_msg.pose.pose.orientation.x,odom_msg.pose.pose.orientation.y,odom_msg.pose.pose.orientation.z,odom_msg.pose.pose.orientation.w)
         # print(rospy.get_rostime(), rospy.get_time(), time.time(), type(rospy.get_rostime()), type(rospy.get_time()))
         # t = odom_msg.header.stamp
         # print(t, t.secs, t.nsecs)
         rate.sleep()

if __name__ == '__main__':
     try:
         talker()
     except rospy.ROSInterruptException:
         pass
