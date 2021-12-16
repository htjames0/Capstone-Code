import rospy 
from std_msgs.msg import String

def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def listener(): 
   rospy.init_node('ultra_list', anonymous=True)
   rospy.Subscriber('ultra_topic', float64, callback)
   rospy.spin()

if __name__ == '__main__': 
   listener()
