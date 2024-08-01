#!usr/bin/env python

import rospy
from std_msgs.msg import String
import subprocess

def read():
    rospy.init.node('yolo_reader', anonymous=True)
    p = rospy.Publisher('yolo_reads', String, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        try:
            process = subprocess.Popen(['roslaunch darknet_ros yolo_v3_tiny.launch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if stdout:
                output = stdout.decode('utf-8')
                rospy.loginfo(f"Command output: {output}")
                p.publish(output)
            if stderr:
                error = stderr.decode('utf-8')
                rospy.logerr(f"Command error: {error}")

        except Exception as e:
            rospy.logerr(f"Failed to run command: {str(e)}")

        rate.sleep()

if __name__ == '__main__':
    try:
        read()
    except rospy.ROSInterruptException:
        pass
