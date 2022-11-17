#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class ImageLines:  # ~~~~~~~~~~~~ Everything needs to be under one callback~~~~~~~~~~~~~~~~~~~~~~~
 def __init__(self):
  rospy.Subscriber("/ms09dom/camera_node/image/compressed",CompressedImage,self.callback, queue_size=1, buff_size=2**24)
   
  self.pubedge = rospy.Publisher("/image_edges",Image, queue_size=10)
  self.publinewhite = rospy.Publisher("/image_lines_white",Image, queue_size=10)
  self.publineyellow = rospy.Publisher("/image_lines_yellow",Image, queue_size=10)
  
  rospy.Subscriber("/image_yellow",Image,self.callbackyellow)
  rospy.Subscriber("/image_white",Image,self.callbackwhite)
  
  self.cannyED = 1 
  
  self.bridge = CvBridge()

 def callback(self,msg):
  cv_img = self.bridge.compressed_imgmsg_to_cv2(msg,"bgr8")
  
  image_size = (160, 120)
  offset = 40
  new_image = cv2.resize(old_image, image_size, interpolation=cv2.INTER_NEAREST)
  cropped_image = new_image[offset:, :]
  
  convert_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
  
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
  kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
  dilated_yellow = cv2.dilate(output_image_yellow, kernal)
  dilated_white = cv2.dilate(output_image_white, kernal)
  
  ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped,"bgr8")
  ros_yellow = self.bridge.cv2_to_imgmsg(dilated_yellow,"mono8")
  ros_white = self.bridge.cv2_to_imgmsg(dilated_white,"mono8")
   
  cannyED = cv2.Canny(cropped_image, 0, 255) #Need to set values between 0-255
  # ~~~~~~~~~~~~~~Is this right?~~~~~~~~~~~~~~~~~
  
  
 ####Draws lines on the cropped image
 def output_lines(self, original_image, lines): #~~~~~~~~~~~~~~~~~~Do I need to get rid of this callback?~~~~~~~~~~
        output = np.copy(original_image)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
                cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
                cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
        return output
 
  
  #Use a mask to combine
  combinedyellow = cv2.bitwise_and(self.cannyED, self.cv_imgyellow)
  combinedwhite = cv2.bitwise_and(self.cannyED, self.cv_imgwhite) 
  
  Houghyellow = cv2.HoughLinesP(combinedyellow, 1, 0.01744, 30, 1, 1)################ need to change last 3 variables
  Houghwhite = cv2.HoughLinesP(combinedwhite, 1, 0.01744, 30, 1, 1)################## "
  
  croppedyellowcombined = self.output_lines(self.cvimg_cropped, Houghyellow)
  croppedwhitecombined = self.output_lines(self.cvimg_cropped, Houghwhite)
  
  ros_cannyED = self.bridge.cv2_to_imgmsg(self.cannyED,"mono8")
  ros_linesyellow = self.bridge.cv2_to_imgmsg(croppedyellowcombined,"bgr8") 
  ros_lineswhite = self.bridge.cv2_to_imgmsg(croppedwhitecombined,"bgr8")
  
  self.pubedge.publish(ros_cannyED)
  self.publineyellow.publish(ros_linesyellow)
  self.publinewhite.publish(ros_lineswhite)
  
if __name__ == '__main__':
 rospy.init_node('image_lines', anonymous=True)
 image_crop = ImageLines()
 
 rospy.spin()
