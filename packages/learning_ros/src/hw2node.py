#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class Talker:
 def __init__(self):
  self.pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
  self.count = 0
 def turtle(self):
 
  self.count +=1
  
  if self.count >0 and self.count <2:
   forward = Twist()
   forward.linear.x = 2
   self.pub.publish(forward)
   rospy.logwarn("Part1")
   
  if self.count >2 and self.count <4:
   turn = Twist()
   turn.angular.z = 1
   self.pub.publish(turn)
   forward = Twist()
   forward.linear.x = 2
   self.pub.publish(forward)
   rospy.logwarn("Part2")
   
  if self.count >4 and self.count <6:
   turn = Twist()
   turn.angular.z = 1
   self.pub.publish(turn)
   forward = Twist()
   forward.linear.x = 2
   self.pub.publish(forward)
   rospy.logwarn("Part3")
   
  if self.count >6 and self.count <8:
   turn = Twist()
   turn.angular.z = 1
   self.pub.publish(turn)
   forward = Twist()
   forward.linear.x = 2
   self.pub.publish(forward)
   rospy.logwarn("Final")

if __name__ == '__main__':
 try:
  rospy.init_node('talker', anonymous=True)
  t = Talker()
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
   t.turtle()
   rospy.logwarn("Test")
   rate.sleep()
 except rospy.ROSInterruptException:
  pass
