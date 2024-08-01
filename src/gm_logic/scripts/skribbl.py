#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from moves_src import GameMoves
import random
import threading

class Logic:
    def __init__(self):
        self.moves = GameMoves()
        rospy.init_node('skribbl_node', anonymous=True)
        rospy.Subscriber("/darknet_ros/object_names", String, self.callback)

        self.last_confirmation = rospy.Time.now()
        self.debounce_time = rospy.Duration(1)

        self.object_list = ['apple', 'donut', 'cake', 'pizza']
        self.detected_objects = []
        self.detected = False
        self.round_active = False
        self.start_round()

    def callback(self, object_names):
        object_names = object_names.data
        if rospy.Time.now() - self.last_confirmation < self.debounce_time:
            return
        
        if self.round_active:
            self.detected_objects.append(object_names)
            if self.selected_object in self.detected_objects:
                self.detected = True
                self.last_confirmation = rospy.Time.now()
                self.round_active = False

    def start_round(self):
        self.detected_objects = []
        self.detected = False
        self.round_active = True

        self.selected_object = random.choise(self.object_list)
        print('draw: ' + str(self.selected_object))

        self.timer_thread = threading.Thread(target=self.start_timer)
        self.timer_thread.start

    def start_timer(self):
        rospy.sleep(20)
        self.check_detection

    def check_detection(self):
        if self.detected:
            print(str(self.selected_object) + ' detected!')
            self.moves.ccw_spin()
        else:
            print('out of time')

if __name__ == '__main__':
    while not rospy.is_shutdown():
        Logic()
        rospy.spin()
    