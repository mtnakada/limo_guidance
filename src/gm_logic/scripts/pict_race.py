#!/usr/bin/env python
import os
import sys
module_path = os.path.expanduser('~/nakada_ws/src/gm_movectrl/src')
if module_path not in sys.path:
    sys.path.append(module_path)

import rospy
import random
from std_msgs.msg import String
from moves_src import GameMoves


class PictRaceGame:
    def __init__(self):
        self.moves = GameMoves()

        self.last_detection = rospy.Time.now()
        self.debounce_time = rospy.Duration(1)

        self.object_list = ['wine glass', 'fork', 'chair', 
                            'clock', 'vase', 'scissors']
        # self.object_list = ['apple', 'donut', 'cake', 'pizza']
        
        self.game_islive = False
        self.current_selection = random.choice(self.object_list)
        self.goal = 3
        self.position = 0
        
    
    def callback(self, object_names):
        object_names = object_names.data
        if rospy.Time.now() - self.last_detection < self.debounce_time:
            return
        
        if self.current_selection in object_names and not self.moves.is_moving:
            self.last_detection = rospy.Time.now()
            print(str(self.current_selection)+' detected! moving forward')
            self.object_list.remove(self.current_selection)
            self.moves.forward()
            self.position += 1

            if self.position >= self.goal:
                self.game_islive = False
                print('win! press "enter" to start again')
                self.current_selection = 'empty'
            else:
                self.new_selection()

    def new_selection(self):
        self.current_selection = random.choice(self.object_list)
        print('draw: ' + str(self.current_selection))

    def start(self):
        self.game_islive = True
        self.object_list = ['wine glass', 'fork', 'chair', 
                            'clock', 'vase', 'scissors']
        self.position = 0
        self.goal = 3
        print('game start!')
        self.new_selection()
        rospy.Subscriber("/darknet_ros/object_names", String, self.callback)

class GameStarter:
    def __init__(self):
        self.game = PictRaceGame()
        rospy.Subscriber("/keyinput", String, self.key_callback)

    def key_callback(self,key):
        key = key.data

        if key == '\r' and not self.game.game_islive:
            self.game.start()
        elif key == '/' and self.game.game_islive:
            self.game.game_islive = False
            print('game interrupted') 
            

if __name__ == '__main__':
    rospy.init_node('pict_race_node', anonymous=True)
    rospy.sleep(10)
    print("press 'enter' to start game")
    g = GameStarter()
    rospy.spin()
