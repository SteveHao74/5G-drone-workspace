#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CompressedImage
import cv2
from cv_bridge import CvBridge
import numpy as np

def callback(imgmsg):
    bridge = CvBridge()
    print(type(imgmsg.data))
    print(len(imgmsg.data)) # 2764800 / 55602
    # buf = np.ndarray(shape=(1, len(imgmsg.data)),dtype=np.uint8, buffer=imgmsg.data)
    # im = cv2.imdecode(buf, cv2.IMREAD_ANYCOLOR)
    # col_img = cv2.imdecode(np.frombuffer(imgmsg.data, dtype='uint8'), cv2.IMREAD_COLOR)
    # print(im.shape, col_img.shape, np.all(im == col_img))

    img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    # img = bridge.imgmsg_to_cv2(imgmsg, '16UC1')
    # img = bridge.compressed_imgmsg_to_cv2(imgmsg, "bgr8")
    # img = bridge.compressed_imgmsg_to_cv2(imgmsg, "passthrough")

    # ret, jpg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    # print(len(img.tobytes()), len(jpg.tobytes()))

    print(img.shape)
    print(img.dtype)
    print('******************')

    # img = cv2.applyColorMap(cv2.convertScaleAbs(img, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imshow("listener", img)
    cv2.waitKey(3)


def callback2(imgmsg):
    bridge = CvBridge()
    # img = bridge.imgmsg_to_cv2(imgmsg, "bgr8")
    # img = bridge.imgmsg_to_cv2(imgmsg, '16UC1')
    # img = bridge.compressed_imgmsg_to_cv2(imgmsg, "bgr8")
    img = bridge.compressed_imgmsg_to_cv2(imgmsg, "passthrough")

    img = cv2.applyColorMap(cv2.convertScaleAbs(img, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imshow("depth_img", img)
    cv2.waitKey(3)


def listener():
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/img_tr", Image, callback)
    # rospy.Subscriber("/camera/fisheye1/image_raw", Image, callback)
    rospy.Subscriber("/camera/color/image_raw", Image, callback) #(720, 1280, 3)
    # rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, callback) #(720, 1280)
    # rospy.Subscriber("/camera/depth/image_rect_raw", Image, callback) #(480, 848)
    # rospy.Subscriber("/camera/color/image_raw/compressed", CompressedImage, callback) #(720, 1280, 3)
    # rospy.Subscriber("/camera/color/image_raw/compressedDepth", CompressedImage, callback)  # (720, 1280, 3)
    # rospy.Subscriber("/camera/aligned_depth_to_color/image_raw/compressed", CompressedImage, callback2)

    rospy.spin()


if __name__ == '__main__':
    listener()
