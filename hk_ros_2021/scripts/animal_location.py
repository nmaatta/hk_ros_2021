#! /usr/bin/env python
import math
import rospy
import tf
import tf2_ros

from sensor_msgs.msg import LaserScan
from darknet_ros_msgs.msg import BoundingBox #msg that contains bounding box coordinates
from darknet_ros_msgs.msg import BoundingBoxes
# from apriltag_ros.msg import Coordinates
#rostopic echo darknet_ros/bounding_boxes...
#std_msgs/Header header
  #uint32 seq
  #time stamp
  #string frame_id
#std_msgs/Header image_header
  #uint32 seq
  #time stamps
  #string frame_id
#darknet_ros_msgs/BoundingBox[] bounding_boxes
  #float64 probability
  #int64 xmin
  #int64 ymin
  #int64 xmax
  #int64 ymax
  #int16 id
  #string Class

#rostopic type /scan | rosmsg show
#std_msgs/Header header
  #uint32 seq
  #time stamp
  #string frame_id
#float32 angle_min
#float32 angle_max
#float32 angle_increment
#float32 time_increment
#float32 scan_time
#float32 range_min
#float32 range_max
#float32[] ranges
#float32[] intensities

rospy.init_node('animalDetect_node',anonymous = False)

# lidar_angle = None

def callback1(animalBox): #function for calculating relative


    #global lidar_angle
    angleScale = 320/26.75  #Camera view 26.75*2, negativ direction counter clockwise

    try:
        animalType = str(animalBox.bounding_boxes[0].Class)



        #CALCULATING
        if animalType in ['cat', 'cow', 'dog', 'horse']: #if class is one of these animals
            print(animalType)
            x_max = animalBox.bounding_boxes[0].xmax
            x_min = animalBox.bounding_boxes[0].xmin

            x_position = (x_max + x_min)/2 #calculate the pixel in optical frame [0-640] Raspery pi has resolut 640x....

            x_angle = x_position/angleScale-26.75
            x_angle = round(x_angle)

            if x_angle <0:               #To get correct slot in ranges[], pos direct in ranges is counter clockwise [0-359]

                lidar_angle = -x_angle
            else:
                lidar_angle = 359 - x_angle


            #print(x_angle)
            # print(lidar_angle)

            # lidarAngleInfo = Coordinates()
            #
            # lidarAngleInfo.lidarAngle = lidar_angle #might be good for geometric
            #
            # try:
            #     pub.publish(lidarAngleInfo)   #Publishing coordinates onto the "chatter" topic for the yaml file to read.
            #
            # except rospy.ROSInterruptException:
            #     pass

            return lidar_angle
        else:
            return

    except (IndexError):
        return

    #TRANSLATE THIS TO ANGLE AROUND ROBOT
        #note: 53.5 degree viewing angle max (-26.75 to 26.75)
        #note: LaserScan (0-360) with 0 being in front, rotating CCW - base scan



def callback2(laserData): #function for determining laser distance at determined angle
#    print len(msg.ranges)

    try:

        x = callback1()
        #x = callback1(animalBox).lidar_angle

        #lidar_angle_new = int(lidar_angle)
        #xx = int(x)
        #print(lidar_angle_new)
        #print(x)
    except:
        pass
    x = callback1()
    #x = callback1().lidar_angle

    #animalDistance = laserData.ranges[xx]
    #print(animalDistance)
    #animalDistance = laserData.ranges[int(lidar_angle)]
    #lidar_angle = None
    #print(animalDistance)

    # if lidar_angle:
    #     print(lidar_angle)

    # try:
    #     animal_distance = laserData.ranges[lidar_angle]
    # # if x_angle:
    #     print(animal_distance)
    #
    # except(IndexError):
    #pub = rospy.Publisher('animalFound', Coordinates, queue_size=10)
    #return

if __name__ == '__main__':



    sub1 = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes , callback1)
    #sub2 = rospy.Subscriber('/scan', LaserScan , callback2)
    # sub3 = rospy.Subscriber('chatter', Coordinates , callback2)
    sub2 = rospy.Subscriber('/scan', LaserScan , callback2)
    rospy.spin() #continuous loop
