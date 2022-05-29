#!/usr/bin/env python
import rospy
from  nav_msgs.msg  import Odometry


def callback(odom_msg):
    print('-----------' * 10)
    rospy.loginfo("Publsh odom message [%1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f, %1.2f]",
                  odom_msg.pose.pose.position.x, odom_msg.pose.pose.position.y, odom_msg.pose.pose.position.z,
                  odom_msg.pose.pose.orientation.x, odom_msg.pose.pose.orientation.y, odom_msg.pose.pose.orientation.z,
                  odom_msg.pose.pose.orientation.w)
    print('***********' * 10)


def listener():
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/odom_tr", Odometry, callback)
    rospy.Subscriber("/camera/odom/sample", Odometry, callback)

    rospy.spin()
    # r = rospy.Rate(10)  # 10hz
    # while not rospy.is_shutdown():
    #     r.sleep()  # time must enough for callback,or it will out while loop
    # rospy.spin()


if __name__ == '__main__':
    listener()
