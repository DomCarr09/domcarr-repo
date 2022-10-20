#!/usr/bin/env python3

import rospy
import math
from turtlesim.msg import Pose
from math import radians, sin, cos
from odometry_hw.msg import DistWheel
from odometry_hw.msg import Pose2D

class Listener:
 def __init__(self):
  rospy.Subscriber("dist_wheel",DistWheel,self.callback)
  
  self.pub = rospy.Publisher("pose",Pose2D, queue_size=10)
  self.pub_pose = Pose2D()
  self.posex = 0
  self.posey = 0
  self.theta = 0
  self.old_theta = 0
  self.deltax = 0
  self.deltay = 0
  self.delta_theta = 0
  self.delta_s = 0
  self.delta_sL = 0
  self.delta_sR = 0 

 def callback(self,Ping):
  self.delta_sL = Ping.dist_wheel_left
  self.delta_sR = Ping.dist_wheel_right
  
  self.delta_s = (self.delta_sL + self.delta_sR)/2
  self.delta_theta = (self.delta_sR - self.delta_sL)/0.1 ####0.1 = 2L
  self.deltax = self.delta_s*cos(self.theta + (self.delta_theta/2))
  self.deltay = self.delta_s*sin(self.theta + (self.delta_theta/2))
  
  self.newposex = self.posex + self.deltax
  rospy.logwarn("Calculated New Pose in x direction")
  self.pub_pose.x = self.newposex
  
  
  self.newposey = self.posey + self.deltay
  rospy.logwarn("Calculated New Pose in y direction")
  self.pub_pose.y = self.newposey
  
  self.newtheta = self.theta + self.delta_theta
  rospy.logwarn("Calculated New Theta")
  self.pub_pose.theta = self.newtheta
  
  self.pub.publish(self.pub_pose)
  
  self.posex = self.newposex
  self.posey = self.newposey
  self.theta = self.newtheta ###Think I did this right?
 
  
if __name__ == '__main__':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
