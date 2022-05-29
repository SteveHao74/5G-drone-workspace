#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np


def talker():
    pub = rospy.Publisher('/img_tr', Image, queue_size=1)
    rospy.init_node('img_tr', anonymous=True)
    rate = rospy.Rate(30)
    bridge = CvBridge()
    Video = cv2.VideoCapture(0)
    # Video = cv2.VideoCapture('1.avi')
    while not rospy.is_shutdown():
        ret, img = Video.read()
        # img = np.zeros((720, 1080, 3), dtype=np.uint8)
        # img = np.random.randint(0, 256, (720, 1080, 3), dtype=np.uint8)
        cv2.imshow("talker", img)
        cv2.waitKey(3)
        # print(img.shape)
        pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
