import rospy
from std_msgs.msg import Float64
import cv2

def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
   if data.data < 100 and data.data > 50:
      print(f'I took a picture and saved it as test.jpg')
      img = cv2.imread(test.jpg)
         
def listener():
   rospy.init_node('cam_list', anonymous=True)
   rospy.Subscriber('ultra_topic', Float64, callback)
   #keeps python from exiting until node is stopped
   rospy.spin()

if __name__ == '__main__':
   listener()
