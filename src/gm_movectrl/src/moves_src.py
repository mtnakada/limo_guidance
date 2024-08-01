import rospy
from geometry_msgs.msg import Twist
import random 

class GameMoves:
    def __init__(self):
        rospy.init_node('pict_race_node', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd_vel = Twist()
        self.rate = rospy.Rate(10)
        self.is_moving = False

    def ccw_spin(self):
        self.is_moving = True
        self.cmd_vel.angular.z = 3.14
        endtime = rospy.Time.now() + rospy.Duration(3)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.angular.z = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False

    def cw_spin(self):
        self.is_moving = True
        self.cmd_vel.angular.z = -3.14
        endtime = rospy.Time.now() + rospy.Duration(3)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.angular.z = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False
    
    def turn_around(self):
        self.is_moving = True
        self.cmd_vel.angular.z = 3.14
        endtime = rospy.Time.now() + rospy.Duration(1.25)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.angular.z = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False

    def left_turn(self):
        self.is_moving = True
        self.cmd_vel.angular.z = 1.5
        self.cmd_vel.linear.x = .25
        endtime = rospy.Time.now() + rospy.Duration(1.5)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.angular.z = 0
        self.cmd_vel.linear.x = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False

    def right_turn(self):
        self.is_moving = True
        self.cmd_vel.angular.z = -1.5
        self.cmd_vel.linear.x = .25
        endtime = rospy.Time.now() + rospy.Duration(1.5)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.angular.z = 0
        self.cmd_vel.linear.x = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False

    def forward(self):
        self.is_moving = True
        self.cmd_vel.linear.x = .25
        endtime = rospy.Time.now() + rospy.Duration(2)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        self.cmd_vel.linear.x = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False

    def cont_forward(self):
        self.cmd_vel.linear.x = .25
        while not rospy.is_shutdown():
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()
    
    def random_turn(self):
        self.is_moving = True
        turntime = random.randint(1,5)
        self.cmd_vel.angular.z = 3.14
        endtime = rospy.Time.now() + rospy.Duration(turntime)
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()
        
        self.cmd_vel.angular.z = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False