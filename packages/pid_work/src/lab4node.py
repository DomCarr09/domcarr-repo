#!/usr/bin/env python3
import rospy
from numpy import arange,sign
from random import random
from duckietown_msgs.msg import AprilTagDetectionArray
from geometry_msgs.msg import Twist
from duckietown_msgs.msg import FSMState
from duckietown_msgs.msg import Twist2DStamped
from geometry_msgs.msg import Quaternion

class PIDControl:
	def __init__(self):
		self.pub = rospy.Publisher('/ms09dom/car_cmd_switch_node/cmd',Twist2DStamped, queue_size=10)
		rospy.Subscriber("/ms09dom/apriltag_detector_node/detections",AprilTagDetectionArray,self.callback)
		self.total_error = 0
		self.time = 0
		self.old_time = 0
		self.old_error = 0
		self.y_old_error = 0
		self.integral = 0
		self.old_integral = 0
		
		self.y_integral = 0
		self.y_old_integral = 0
		
		self.kp_turning = 1 # 1
		self.ki_turning = 0.2 #0.
		self.kd_turning = 0.5 #0.5
		
		self.kp_forward = 0.2 #0.25
		self.ki_forward = 0.01 #0.15
		self.kd_forward = 0.5 #0.5
		
		self.turning_error = 0
		self.forward_error = 0 #Will need to add this

	def callback(self,Ping):
		turn = Twist2DStamped()
		forward = Twist2DStamped()
		stop = Twist2DStamped()
		for detect in Ping.detections:
			if detect:
				x1 = detect.transform.translation.x
				y1 = detect.transform.translation.z
				
				if(x1 != 0):
					#rospy.logwarn("Begin Callback: " + str(x1))
					self.time = rospy.get_time()
					delta_time = self.time - self.old_time
					
					#Turning~~~~~~~~
					if delta_time < 1:
						rospy.logwarn("Start")
						self.turning_error = -x1
						self.integral = (self.turning_error*delta_time) + self.old_integral
						self.old_integral = self.integral
					
					p = (self.kp_turning*self.turning_error)
					i = (self.ki_turning*self.integral)
					d = self.kd_turning*((self.turning_error - self.old_error)/(delta_time))
					self.total_error_turning = p + i + d
					
					turn.omega = 0.8*self.total_error_turning
					self.pub.publish(turn)
					rospy.logwarn("Turn published")
					self.old_time = self.time
					self.old_error = self.turning_error
				
				if (not(y1<0.1 and y1 > 0.12)):
					#rospy.logwarn("Begin Callback: " + str(y1))
					self.time = rospy.get_time()
					delta_time = self.time - self.old_time
					
					#Turning~~~~~~~~
					if delta_time < 1:
						rospy.logwarn("Start")
						self.forward_error = y1 - 0.08
						self.y_integral = (self.forward_error*delta_time) + self.y_old_integral
						self.y_old_integral = self.y_integral
					
					p1 = (self.kp_forward*self.forward_error)
					i1 = (self.ki_forward*self.y_integral)
					d1 = self.kd_forward*((self.forward_error - self.y_old_error)/(delta_time))
					self.total_error_forward = p1 + i1 + d1
					
					forward.v = 0.5*self.total_error_forward
					self.pub.publish(forward)
					rospy.logwarn("Forward published")
					self.old_time = self.time
					self.y_old_error = self.forward_error
				
				
				'''
			if len(Ping.detections)==0:
				stop.v = 0
				stop.omega = 0
				self.pub.publish(stop)
				rospy.logwarn("Stop published")
				'''
if __name__ == '__main__':
	rospy.init_node('pid_control', anonymous=True)
	PIDControl()
	rospy.spin()

