#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def fullturn():
    rospy.init_node('fullturn_node', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    rate = rospy.Rate(10)
    
    move_cmd = Twist()
    move_cmd.angular.z = -3.14

    rospy.loginfo("turning once")
    turntime = 4
    endtime = rospy.Time.now() + rospy.Duration(turntime)
    while rospy.Time.now() < endtime:
        pub.publish(move_cmd)
        rate.sleep()
        
    move_cmd.angular.z = 0
    pub.publish(move_cmd)

if __name__ == '__main__':
    try:
        fullturn()
    except rospy.ROSInterruptException:
        pass