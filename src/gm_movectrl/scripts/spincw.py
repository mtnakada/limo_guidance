#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def spincw():
    rospy.init_node('spincw_node', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    rate = rospy.Rate(10)

    move_cmd = Twist()
    move_cmd.angular.z = -1

    rospy.loginfo("spinning clockwise")

    while not rospy.is_shutdown():
        pub.publish(move_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        spincw()
    except rospy.ROSInterruptException:
        pass