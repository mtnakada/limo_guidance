#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from functools import partial

def key_callback(cmd_vel, key):
    key = key.data
    if key == 'w':
        cmd_vel.linear.x = 1
    else:
        cmd_vel.linear.x = 0

def main():
    rospy.init_node('manualforward_node', anonymous=True)
    cmd_vel = Twist()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('keyinput', String, partial(key_callback, cmd_vel) )
    rate = rospy.Rate(10)

    print('w to go forward, any other key to stop')

    while not rospy.is_shutdown():
        pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass