#!/usr/bin/env python3

import rospy
import math

from turtlesim_helper.msg import UnitsLabelled

class Listener:#
 def __init__(self):
  self.pub = rospy.Publisher('/HW4Topic',UnitsLabelled, queue_size=10)
  self.pub_msg = UnitsLabelled()
  self.pub_msg.units = "meters"
  rospy.Subscriber("turtlesim_helper/UnitsLabelled",UnitsLabelled,self.callback)


 def callback(self,Pong): 
  if rospy.has_param("mode1"):
   mode1 = rospy.get_param("mode1")

   if mode1 == "meters":
    self.M = Pong.value
    rospy.logwarn("Converted")
    self.pub_msg.value = self.M
    self.pub.publish(self.pub_msg)

   if mode1 == "feet":
    self.F = Pong.value*3.281
    rospy.logwarn("Converted")
    self.pub_msg.value = self.F
    self.pub_msg.units = "feet"
    self.pub.publish(self.pub_msg)

   if mode1 == "smoots":
    self.S = Pong.value/1.702
    rospy.logwarn("Converted")
    self.pub_msg.value = self.S
    self.pub_msg.units = "smoots"
    self.pub.publish(self.pub_msg)
   


if __name__=='__main__':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
