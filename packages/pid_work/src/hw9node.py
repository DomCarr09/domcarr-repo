#!/usr/bin/env python3
import rospy
from numpy import arange,sign
from random import random
from std_msgs.msg import Float32

class PIDControl:
 def __init__(self):
  self.pub = rospy.Publisher('control_input',Float32, queue_size=10) #right?
  rospy.Subscriber("error",Float32,self.callback) #not sure if I did this right
  
  self.total_error = 0
  self.time = 0
  self.old_time = 0
  self.old_error = 0
  self.integral = 0
  self.old_integral = 0
  self.kp = 0.225
  self.ki = 0.005
  self.kd = 0.55
  
  ready = rospy.set_param("controller_ready", 'true')
 
 def callback(self,Ping):
  self.time = rospy.get_time()
  delta_time = self.time - self.old_time #having trouble thinking about how to get the elapsed time properly
  
  
  if delta_time < 1:
   self.integral = (Ping.data*delta_time) + self.old_integral #Ping.data = error
   self.old_integral = self.integral
  
  
  self.total_error = (self.kp*Ping.data) + (self.ki*self.integral) + self.kd*((Ping.data - self.old_error)/(delta_time))
  
  self.pub.publish(self.total_error)
  rospy.logwarn("Calulated")
  rospy.logwarn(self.total_error)
   
  self.old_time = self.time
  self.old_error = Ping.data
  
  
if __name__ == '__main__':
 rospy.init_node('pid_control', anonymous=True)
 PIDControl()
 
 rospy.spin()
