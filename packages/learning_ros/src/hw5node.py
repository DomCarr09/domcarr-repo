#!/usr/bin/env python3

import rospy
import math
import numpy
from math import radians, sin, cos
from duckietown_msgs.msg import Vector2D

class Listener:
 def __init__(self):
  rospy.Subscriber("/sensor_coord",Vector2D,self.callback)
  
  self.pub1 = rospy.Publisher('/robot_coord',Vector2D, queue_size=10)
  self.pub_msg = Vector2D()
  self.Trs = numpy.matrix([[-1,0,-1],[0,-1,0],[0,0,1]])

  self.pub2 = rospy.Publisher('/world_coord',Vector2D, queue_size=10)
  self.Twr = numpy.matrix([[-math.sqrt(2)/2,-math.sqrt(2)/2,5],[math.sqrt(2)/2,-math.sqrt(2)/2,3],[0,0,1]])
 
 def callback(self,msg):
  self.pointA = [[msg.x],[msg.y],[1]]
  
  rospy.logwarn("Position relative to robot")
  self.Pra = self.Trs*self.pointA
  self.pub_msg.x = self.Pra[0,0]
  self.pub_msg.y = self.Pra[1,0]
  self.pub1.publish(self.pub_msg)
  
  rospy.logwarn("Position relative to world")
  self.Pwa = self.Twr*self.Pra
  self.pub_msg.x = self.Pwa[0,0]
  self.pub_msg.y = self.Pwa[1,0]
  self.pub2.publish(self.pub_msg)
  
  
  
if __name__ == '__main__':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
