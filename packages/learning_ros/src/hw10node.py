#!/usr/bin/env python3

import rospy
import actionlib
import example_action_server.msg
from example_service.srv import Fibonacci, FibonacciResponse

###### Note ######
# There were no errors when doing roslaunch, but it is also not outputting anything and I'm not sure how to fix it
# What I was trying to do is combine the example codes into one node and then alter them, but I unfortunatly still am
# unsure about how they work so I was unable to debug the code properly.

class FibonacciService:
    def __init__(self):
        self.calc_fibonacci = rospy.Service('calc_fibonacci', Fibonacci, self.handle_calc_fibonacci)
    def handle_calc_fibonacci(self,req):
        r = rospy.Rate(1)
        sequence = [0,3]
        r.sleep()
        if req.order == 3:
            return FibonacciResponse(sequence[0:3])
        r.sleep()
        for i in range(1,req.order):
            sequence.append(sequence[i] + sequence[i-1]) #I'm not exactly sure what this does...
            r.sleep()
        return FibonacciResponse(sequence)
        rospy.loginfo("Time for Service, Order 3")
        
        
        r = rospy.Rate(1)
        sequence = [0,15]
        r.sleep()
        if req.order == 15:
            return FibonacciResponse(sequence[0:15])
        r.sleep()
        for i in range(1,req.order):
            sequence.append(sequence[i] + sequence[i-1]) #I'm not exactly sure what this does...
            r.sleep()
        return FibonacciResponse(sequence)
        rospy.loginfo("Time for Service, Order 15")
        
        #Is this supposed to do a sequence based on the time that has passed?
        #I'm not sure how to change this like the action client to do 3 and 15
        #I feel like this could be simplier, but I'm still not sure how the services and clients work

def fibonacci_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    print("starting client")
    client = actionlib.SimpleActionClient('fibonacci', example_action_server.msg.FibonacciAction)

    print("waiting for server")
    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    
    print("sending goal")
    # Creates a goal to send to the action server.
    goal = example_action_server.msg.FibonacciGoal(order=3) #~~~~~~~~~~ 3 Order

    # Sends the goal to the action server.
    client.send_goal(goal)

    print("waiting for result")
    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult
    rospy.loginfo("Time for Action Client, Order 3")
    
    
    
    client = actionlib.SimpleActionClient('fibonacci', example_action_server.msg.FibonacciAction)

    print("waiting for server")
    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    
    print("sending goal")
    # Creates a goal to send to the action server.
    goal = example_action_server.msg.FibonacciGoal(order=15) #~~~~~15 order

    # Sends the goal to the action server.
    client.send_goal(goal)

    print("waiting for result")
    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult
    rospy.loginfo("Time for Action Client, 15 Order 3")
    
    

if __name__ == '__main__':
    try:
        rospy.init_node('fibonacci_service_node') #I'm not sure if this is right either, I tried to combine the two.
        FibonacciService()
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        #rospy.init_node('fibonacci_client_py') #This was giving me an error, saying it was already started with different arguments
        result = fibonacci_client()
        print("Result:", ', '.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
    rospy.spin()
