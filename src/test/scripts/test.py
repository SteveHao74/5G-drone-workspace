import message_filters
from std_msgs.msg import Int32, Float32
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import cv2
import rospy
import numpy as np

# def callback(mode, penalty):
#   # The callback processing the pairs of numbers that arrived at approximately the same time
#     return
#
# mode_sub = message_filters.Subscriber('/img_tr', Image)
# penalty_sub = message_filters.Subscriber('/odom_tr', Odometry)
#
# ts = message_filters.ApproximateTimeSynchronizer([mode_sub, penalty_sub], 10, 0.1, allow_headerless=True)
# ts.registerCallback(callback)
# rospy.spin()

while True:
    img = np.random.randint(0, 65536, (480, 640), dtype=np.uint16)
    b = img.tobytes()
    c = np.frombuffer(b, np.uint16).reshape(480, 640)
    ret, png = cv2.imencode('.png', img)

    img1 = np.uint8(img & 0x00ff)
    img2 = np.uint8(img >> 8)
    ret, jpg1 = cv2.imencode('.jpg', img1, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    ret, jpg2 = cv2.imencode('.jpg', img2, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    print(len(img.tobytes()), len(png.tobytes()), len(jpg1.tobytes()) + len(jpg2.tobytes()))

    dec1 = cv2.imdecode(jpg1, cv2.IMREAD_ANYDEPTH)
    dec2 = cv2.imdecode(jpg2, cv2.IMREAD_ANYDEPTH)
    dep_img = (np.uint16(dec2) << 8) + dec1
    print(dep_img.shape, dep_img.dtype)
    print(np.sum(img == dep_img))
    break
    img_vis = cv2.applyColorMap(cv2.convertScaleAbs(img, alpha=0.03), cv2.COLORMAP_JET)
    dep_img_vis = cv2.applyColorMap(cv2.convertScaleAbs(dep_img, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imshow('img', img_vis)
    cv2.imshow('dep_img', dep_img_vis)
    cv2.waitKey(10)

# img = np.array([[1,2,3],[65535,65534,65533]], dtype=np.uint16)
# print(img)
# img1 = img & 0x00ff
# img2 = img >> 8
# print(img1, img1.dtype)
# print(img2, img2.dtype)
# h, w = img.shape
# new_img = np.zeros([h, w, 2], dtype=np.uint8)
# # new_img = np.array([img1, img2], dtype=np.uint8)
# new_img[:, :, 0] = img1
# new_img[:, :, 1] = img2
# print(new_img, new_img.shape, new_img.dtype)