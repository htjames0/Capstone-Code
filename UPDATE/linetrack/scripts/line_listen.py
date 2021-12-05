#!usr/bin/env python
import rospy
from std_msgs.msg import Float64

def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.data)

def listener():
   rospy.init_node('linetracker_list', anonymous = True)
   rospy.Subscriber("ultra_topic", Float64, callback)
   rospy.spin()
   
   

if __name__ == '__main__':
   listener()
