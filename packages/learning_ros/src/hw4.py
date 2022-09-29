#!/usr/bin/env python3

import rospy
import math

from turtlesim_helper.msg import UnitsLabelled

class Listener:#
 def init(self):
  self.pub = rospy.Publisher('HW4Topic',UnitsLabelled, queue_size=10)
  self.pub_msg = UnitsLabelled()
  self.pub_msg.units = "meters"
  rospy.Subscriber("turtlesim_helper/UnitsLabelled",UnitsLabelled,self.callback)


 def callback(self,Pong): 
  if rospy.has_param("mode1"):
   mode1 = rospy.get_param("mode1")

   if mode1 == "meters":
    self.M = self.dist
    rospy.logwarn("Converted")
    self.pub_msg.value = self.M
    self.pub.publish(self.pub_msg)

    else:
     rospy.logwarn("Error with meters conversion")

   if mode1 == "feet":
     self.F = self.dist*3.281
     rospy.logwarn("Converted")
     self.pub_msg.value = self.F
     self.pub.publish(self.pub_msg)

    else:
     rospy.logwarn("Error with feet conversion")

   if rospy.has_param("mode3"):
    self.S = self.dist/1.702
    rospy.logwarn("Converted")
    self.pub_msg.value = self.S
    self.pub.publish(self.pub_msg)
     else:
      rospy.logwarn("Error with smoots conversion")


if name == 'main':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
