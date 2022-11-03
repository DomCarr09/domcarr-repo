#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class ImageLines:
 def __init__(self):
  rospy.Subscriber("/image_cropped",Image,self.callback)
  
  self.pubedge = rospy.Publisher("/image_edges",Image, queue_size=10)
  self.publinewhite = rospy.Publisher("/image_lines_white",Image, queue_size=10)
  self.publineyellow = rospy.Publisher("/image_lines_yellow",Image, queue_size=10)
  
  rospy.Subscriber("/image_yellow",Image,self.callbackyellow)
  rospy.Subscriber("/image_white",Image,self.callbackwhite)
  
  self.cannyED = 1 
  
  self.bridge = CvBridge()
 
 #####Cropped Callback 
 def callback(self,msg):
  self.cvimg_cropped = self.bridge.imgmsg_to_cv2(msg,"bgr8") 
  self.cannyED = cv2.Canny(self.cvimg_cropped, 0, 255) #Need to set values between 0-255
  
 #####Yellow Callback
 def callbackyellow(self,msg):
  self.cv_imgyellow = self.bridge.imgmsg_to_cv2(msg,"mono8")
  
 
 ####Draws lines on the cropped image
 def output_lines(self, original_image, lines):
        output = np.copy(original_image)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv2.line(output, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
                cv2.circle(output, (l[0],l[1]), 2, (0,255,0))
                cv2.circle(output, (l[2],l[3]), 2, (0,0,255))
        return output
 
 
 #####White Callback 
 def callbackwhite(self,msg): ###Need multiple callbacks
  self.cv_imgwhite= self.bridge.imgmsg_to_cv2(msg,"mono8")
  
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
