#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def callback(imgmsg):
    bridge = CvBridge()
    # img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    img = bridge.imgmsg_to_cv2(imgmsg, '16UC1')
    ret, jpg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    print(len(img.tobytes()), len(jpg.tobytes()))
    # img = cv2.applyColorMap(cv2.convertScaleAbs(img, alpha=0.03), cv2.COLORMAP_JET)
    img = cv2.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)

    # print('******************')
    print(img.shape)
    # print(img.dtype)

    cv2.imshow("listener", img)
    cv2.waitKey(3)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/img_tr", Image, callback)
    # rospy.Subscriber("/camera/fisheye1/image_raw", Image, callback)
    # rospy.Subscriber("/camera/color/image_raw", Image, callback)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    listener()
