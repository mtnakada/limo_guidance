#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from functools import partial

def yolo_callback(cmd_vel, object_name):
    object_name = object_name.data
    if 'bottle' in object_name:
        cmd_vel.linear.x = 1
        print("go")
    else:
        cmd_vel.linear.x = 0

def main():
    rospy.init_node('yolo_input_test', anonymous=True)
    cmd_vel = Twist()
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('darknet_ros/object_names', String, partial(yolo_callback, cmd_vel) )
    rate = rospy.Rate(10)

    print('moving forward when object name is bottle')

    while not rospy.is_shutdown():
        pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass