#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def straight():
    rospy.init_node('straight_node', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    rate = rospy.Rate(10)

    move_cmd = Twist()
    move_cmd.linear.x = 1

    rospy.loginfo("driving straight")

    while not rospy.is_shutdown():
        pub.publish(move_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        straight()
    except rospy.ROSInterruptException:
        pass