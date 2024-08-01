#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Logic:
    def __init__(self):
        rospy.init_node('cont_guidance', anonymous=True)
        rospy.Subscriber("/darknet_ros/object_names", String, self.callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self.cmd_vel = Twist()
        self.rate = rospy.Rate(10)

        self.last_detection = rospy.Time.now()
        self.timeout = rospy.Duration(0.5)
    
    def callback(self, object_names):
        object_names = object_names.data
        self.cmd_vel = Twist()
        self.last_detection = rospy.Time.now()

        if 'donut' in object_names:
            self.cmd_vel.linear.x = 0.25
            self.cmd_vel.angular.z = 0
        elif 'pizza' in object_names:
            self.cmd_vel.linear.x = 0.25
            self.cmd_vel.angular.z = 1
        elif 'apple' in object_names:
            self.cmd_vel.linear.x = 0.25
            self.cmd_vel.angular.z = -1
        elif 'cake' in object_names:
            self.cmd_vel.linear.x = -.25
            self.cmd_vel.angular.z = 0
        else:
            self.cmd_vel.linear.x = 0
            self.cmd_vel.angular.z = 0

    def run(self):
        print('ready!')
        print('forward: donut, left: pizza, right: apple, backwards: cake')
        while not rospy.is_shutdown():
            if rospy.Time.now() - self.last_detection > self.timeout:
                self.cmd_vel = Twist()
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

if __name__ == '__main__':
    logic = Logic()
    logic.run()
