#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys, termios, tty

class KeyIn:
    def __init__(self):
        self.pub = rospy.Publisher('keyinput', String, queue_size=10)
        rospy.init_node('key_input', anonymous=True)
        self.rate = rospy.Rate(10)

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key
    
    def run(self):
        # print('ctrl+c to quit')
        while not rospy.is_shutdown():
            key = self.get_key()
            if key == '\x03':
                break
            self.pub.publish(key)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        keyop = KeyIn()
        keyop.run()
    except rospy.ROSInterruptException:
        pass