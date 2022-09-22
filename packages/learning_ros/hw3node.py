#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim_helper.msg import UnitsLabelled
class Listener:
 def __init__(self):
  self.pub = rospy.Publisher('turtlesim_helper/UnitsLabelled',UnitsLabelled, queue_size=10)
  self.pub_msg = UnitsLabelled()
  self.pub_msg.units = "meters"
  rospy.Subscriber("/turtlesim/sim",Pose,self.callback) #Need to change the " part, need to listen to Pose, rostopic while running to see too
  self.dist = 0
  Ping.x = 0
  Ping.y = 0
  self.oldx = 0
  self.oldy = 0
 
 def callback(self,Ping): #Can rename Ping anything if want/need
  self.dist = sqrt((Ping.x - sefl.oldx)^2 + (Ping.y-self.oldy)^2)
  self.oldx = Ping.x
  self.oldy = Ping.y
  
  rospy.logwarn("Calulated")
  self.pub_msg.value = self.dist
  self.pub.publish(self.pub_msg)
 
  
if __name__ == '__main__':
 rospy.init_node('listener', anonymous=True)
 Listener()
 
 rospy.spin()
