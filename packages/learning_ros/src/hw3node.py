#!/usr/bin/env python3

import rospy
import math
from turtlesim.msg import Pose
from turtlesim_helper.msg import UnitsLabelled
class Listener:
 def __init__(self):
  self.pub = rospy.Publisher('turtlesim_helper/UnitsLabelled',UnitsLabelled, queue_size=10)
  self.pub_msg = UnitsLabelled()
  self.pub_msg.units = "meters"
  rospy.Subscriber("/turtlesim/turtle1/pose",Pose,self.callback)
  self.dist = 0
  self.oldx = 0
  self.oldy = 0
 
 def callback(self,Ping): #Can rename Ping anything if want/need
  self.dist += math.sqrt((Ping.x - self.oldx)**2 + (Ping.y-self.oldy)**2)
  self.oldx = Ping.x
  self.oldy = Ping.y
  
  rospy.logwarn("Calulated")
  self.pub_msg.value = self.dist
  self.pub.publish(self.pub_msg)
 
  
if __name__ == '__main__':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
