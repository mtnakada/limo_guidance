#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import curses

def keyboard_publisher(stdscr):
    rospy.init_node('key_input', anonymous=True)
    pub = rospy.Publisher('keyinput', String, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr("Press keys to send to the topic. Press 'q' to quit.\n")

    while not rospy.is_shutdown():
        try:
            key = stdscr.getch()
            if key != -1:
                key_str = chr(key)
                if key_str == 'q':
                    break
                pub.publish(key_str)
                stdscr.addstr("Publishing: {}\n".format(key_str))
                stdscr.refresh()
            rate.sleep()
        except rospy.ROSInterruptException:
            break

if __name__ == '__main__':
    try:
        curses.wrapper(keyboard_publisher)
    except rospy.ROSInterruptException:
        pass
