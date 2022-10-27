#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageCropper:
 def __init__(self):
  rospy.Subscriber("/image",Image,self.callback)
  
  self.pub = rospy.Publisher("/image_cropped",Image, queue_size=10)
  self.pub2 = rospy.Publisher("/image_white",Image, queue_size=10)
  self.pub3 = rospy.Publisher("/image_yellow",Image, queue_size=10)
  
  self.bridge = CvBridge()

 def callback(self,msg):
  cv_img = self.bridge.imgmsg_to_cv2(msg,"bgr8")
  
  img_dim = cv_img.shape
  self.end_y = (img_dim[0])
  self.start_y = int(img_dim[0]/2)
  self.end_x = img_dim[1]
  cv_cropped = cv_img[self.start_y:self.end_y, 0:self.end_x]
  
  convert_image = cv2.cvtColor(cv_cropped, cv2.COLOR_BGR2HSV)
  
  output_image_yellow = cv2.inRange(convert_image, (30,160,100), (31,255,255))
  output_image_white = cv2.inRange(convert_image, (40,0,180), (255,255,255))
  #### Need (x,y,z)
  #Need to guess for colors
  
  #output_image = cv2.inRange(input_image, lower_bound, upper_bound)
  
  ######Need to do below for both
  
  ##Erosion
  #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
  #image_erode = cv2.erode(image,kernal) ###########change this to same value as input image?
  
  ##OR
  
  ##Dilation
  #kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  #IMAGE_DILATE = cv2.dilate(image, kernal)
  
  ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped,"bgr8")
  ros_yellow = self.bridge.cv2_to_imgmsg(output_image_yellow,"mono8")
  ros_white = self.bridge.cv2_to_imgmsg(output_image_white,"mono8")
  
  self.pub.publish(ros_cropped)
  self.pub3.publish(ros_yellow)
  self.pub2.publish(ros_white)
 
  
if __name__ == '__main__':
 rospy.init_node('image_cropper', anonymous=True)
 image_crop = ImageCropper()
 
 rospy.spin()
