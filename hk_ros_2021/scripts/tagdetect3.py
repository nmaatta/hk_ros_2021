#!/usr/bin/env python
import rospy
import math
import tf
import geometry_msgs.msg
import tf2_ros
from std_msgs.msg import String
#from nav_msgs.msg import Odometry
#from tf.msg import tfMessage

#from apriltag_ros import ApriltagDetectionArray
#from geometry_msgs import PoseWithCovariance
#from AprilTagDetectionArray.msg import AprilTagDetection
#include <apriltags_ros/AprilTagDetectionArray.h>
from apriltag_ros.msg import AprilTagDetectionArray
from apriltag_ros.msg import Coordinates
from std_msgs.msg import String


rospy.init_node('AprilTagcoords',anonymous = True)
list = tf.TransformListener()

def callback(detectionarray):


    #pub = rospy.Subscriber('tag_detections', AprilTagDetection , chatter_callback)
    #rospy.init_node('odom_tag9',anonymous = True)
    #msg = rospy.wait_for_message("/tag_detections", Pose)
    pub = rospy.Publisher('AprilTag_chatter', Coordinates, queue_size=10)  #Create a chatter node, so we can retrieve coordinates into yaml file
    #rospy.init_node('talker', anonymous=True)
    #list = tf.TransformListener()
    #rate = rospy.Rate(1) # 10hz

    #rate = rospy.Rate(1) #one message per second

    try:
        frame_id = str(detectionarray.detections[0].id)  #Getting the tag number number out of frame_id
        tag_frame = "tag_"+frame_id[1:2]      #making string in format tag_(tagnumber)

        list.waitForTransform('/odom', tag_frame, rospy.Time(), rospy.Duration(1)) #Waiting for a bit to get rid of errors
        (trans,rot) = list.lookupTransform( '/static_frame',tag_frame , rospy.Time(0)) #performing the transformation

        x = trans[0]           #Multiply with -1 to transform the given coordinates
        y = trans[1]           #to match the odom frame orientation


        #return coordinates

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, IndexError):
        return
    #return coordinates

    coordinates_info = Coordinates()

    coordinates_info.x_coord = x
    coordinates_info.y_coord = y
    coordinates_info.tag = tag_frame

    try:
        pub.publish(coordinates_info)   #Publishing coordinates onto the "chatter" topic for the yaml file to read.

    except rospy.ROSInterruptException:
        pass


    #tag_frame = "tag_"+frame_id[1:2]        #Getting the number out of frame_id
    #print(frame_id)
    #print(tag_frame
    #list.waitForTransform('/odom', tag_frame, rospy.Time(), rospy.Duration(1))
    #(trans,rot) = list.lookupTransform( '/odom',tag_frame , rospy.Time(0))
#!/usr/bin/env python
# license removed for brevity

    #x = str(trans[0]*(-1))            #Multiply with -1 to transform the given coordinates
    #y = str(trans[1]*(-1))            #to match the odom frame orientation


    #coordinates = (x + ", " + y)
    #print(coordinates)
    #return coordinates
    #return coordinates

    #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, IndexError):
        #pass

        #print '[',trans[0]*(-1),',',trans[1]*(-1),']'

        #x = str(trans[0]*(-1))            #Multiply with -1 to transform the given coordinates
        #y = str(trans[1]*(-1))            #to match the odom frame orientation
    #oordinates = (x + ", " + y)

        #rate.sleep()
	#print coordinates
	#return coordinates

#def listener():
   #try:
	    #rospy.init_node('odom_tag9',anonymous = True)

        #pub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray , callback)

   #rate = rospy.Rate(1) # 10hz
        #rospy.spin()
   #except rospy.ROSInterrupException:
      #rospy.loginfo("node terminated.")

if __name__ == '__main__':

    #rospy.init_node('odom_tag9',anonymous = True)

    pub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray , callback)

   #rate = rospy.Rate(1) # 10hz
    rospy.spin()
