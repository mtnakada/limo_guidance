#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class DetectControl:
    def __init__(self):
        rospy.init_node('confirm_detection_spin', anonymous=True)
        rospy.Subscriber("darknet_ros/object_names", String, self.yolo_callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        self.is_moving = False
        self.movement_time = rospy.Duration(3.5)
        self.cmd_vel = Twist()
        self.rate = rospy.Rate(10)
        self.last_confirmation = rospy.Time.now()
        self.debounce_time = rospy.Duration(1)
        self.dcount = 0
        self.last_detection = rospy.Time.now()

    def yolo_callback(self, object_name):
        object_name = object_name.data

        if rospy.Time.now() - self.last_confirmation < self.debounce_time:
            return
       
        if 'bottle' in object_name and not self.is_moving:
            print('bottle detected: '+ str(self.dcount))
            self.dcount += 1
            self.last_detection = rospy.Time.now()
            
        if rospy.Time.now() - self.last_detection > self.debounce_time and self.dcount <=20:
            self.dcount = 0
            return
    
        if self.dcount > 20:
            print('bottle confirmed, spinning once')
            self.dcount = 0
            self.is_moving = True
            self.start_spin()
            self.last_confirmation = rospy.Time.now() 
            
    def start_spin(self):
        self.cmd_vel.angular.z = 3.14
        endtime = rospy.Time.now() + self.movement_time
        while rospy.Time.now() < endtime:
            self.pub.publish(self.cmd_vel)
            self.rate.sleep()

        print("done")
        self.cmd_vel.angular.z = 0
        self.pub.publish(self.cmd_vel)
        self.is_moving = False
        self.rate.sleep()
        
    def run(self):
        print("waiting for bottle")
        while not rospy.is_shutdown():
            if not self.is_moving:
                self.cmd_vel.angular.z = 0
                self.pub.publish(self.cmd_vel)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        control = DetectControl()
        control.run()  
    except rospy.ROSInterruptException:
        pass