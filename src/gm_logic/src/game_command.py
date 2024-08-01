#!/usr/bin/env python

import rospy 
from std_msgs.msg import String 
from moves_src import GameMoves
from collections import deque
import threading

class GuidedGame:
    def __init__(self):
        self.moves = GameMoves()
        rospy.Subscriber("/darknet_ros/object_names", String, self.callback)
        rospy.Subscriber("/keyinput", String, self.manager)
        self.game_islive = False

        self.object_map = {
            'cake': self.moves.turn_around,
            'pizza': self.moves.left_turn,
            'apple': self.moves.right_turn,
            'scissors': self.moves.inc_speed,
            'chair': self.moves.dec_speed,
            'wine glass': self.moves.end_game
        }

        self.last_confirmation = rospy.Time.now()
        self.debounce_time = rospy.Duration(1)
        self.move_queue = deque()
        self.start_time = rospy.Time.now()

        self.last_detection = {}
        self.dcount = {obj: 0 for obj in self.object_map.keys()}

        self.lock = threading.Lock()
        self.processing_thread = threading.Thread(target=self.process_queue)
        self.processing_thread.start()
    
    def callback(self, object_names):
        object_names = object_names.data
        now = rospy.Time.now()

        if self.game_islive:
            if now - self.last_confirmation < self.debounce_time:
                return
            
            for object in self.object_map.keys():
                if object in object_names and not self.moves.is_moving:
                    if object not in self.last_detection:
                        self.last_detection[object] = now

                    self.dcount[object] += 1
                    self.last_detection[object] = now
                    print(str(object) + ' detected: ' + str(self.dcount[object]))

                    if self.dcount[object] == 3:
                        print(str(object) + ' confirmed, queuing command')
                        self.dcount[object] = 0
                        # self.object_map[object]()
                        self.move_queue.append(self.object_map[object])
                        # print(self.move_queue)
                        self.last_confirmation = now

            for object in self.object_map.keys():
                if now - self.last_detection.get(object, now) > self.debounce_time and self.dcount[object] <= 15:
                    self.dcount[object] = 0
                    return
    
    def process_queue(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self.game_islive:
                with self.lock:
                    if not self.moves.is_moving and self.move_queue:
                        command = self.move_queue.popleft()
                        print('starting ' + command.__name__)
                        command()
                    elif not self.move_queue:
                        self.cont_forward()
            rate.sleep()

    def cont_forward(self):
        self.moves.cmd_vel.linear.x = self.moves.c_speed
        self.moves.pub.publish(self.moves.cmd_vel)
    
    def fullstop(self):
        self.moves.cmd_vel.linear.x = 0
        self.moves.cmd_vel.angular.z = 0
        self.moves.pub.publish(self.moves.cmd_vel)
        
    def manager(self, key):
        key = key.data
        if key == '\r' and not self.game_islive:
            self.game_islive = True
            print('going!')
            self.start_time = rospy.Time.now()
        elif key == '/' and self.game_islive:
            self.game_islive = False
            self.fullstop()
            print('game interrupted')
        elif key == 'over' and self.game_islive:
            self.game_islive = False
            self.fullstop()
            game_time = rospy.Time.now() - self.start_time
            print('goal reached! time to goal: ' + str(game_time.to_sec()))


if __name__ == '__main__':
    rospy.init_node('game_command', anonymous=True)
    GuidedGame()
    rospy.sleep(8)
    print('press "enter" to start')
    rospy.spin()
