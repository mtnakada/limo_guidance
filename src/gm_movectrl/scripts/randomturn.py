#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import random

def randomturn():
    rospy.init_node('randomturn_node', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    rate = rospy.Rate(10)
    
    move_cmd = Twist()
    move_cmd.angular.z = -6.28

    turntime = random.randint(1,5)
    rospy.loginfo("turning for " + str(turntime) + " seconds")
    endtime = rospy.Time.now() + rospy.Duration(turntime)
    while rospy.Time.now() < endtime:
        pub.publish(move_cmd)
        rate.sleep()
        
    move_cmd.angular.z = 0
    pub.publish(move_cmd)

if __name__ == '__main__':
    try:
        randomturn()
    except rospy.ROSInterruptException:
        pass