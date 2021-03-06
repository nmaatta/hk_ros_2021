#! /usr/bin/env python
import math
import rospy
import tf
import tf2_ros

from sensor_msgs.msg import LaserScan

from apriltag_ros.msg import geometricpixels
from apriltag_ros.msg import geometricrelcoords
from std_msgs.msg import String
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

rospy.init_node('Shapepixelcoords',anonymous = False)

# lidar_angle = None
class lidar:
    def __init__(self):
        self.lidar_angle = None
        self.ranges = []
        self.new_value = 0 #Not used
        self.animaltag = None
    def callback1(self, geometricBox): #function for calculating relative

        angleScale = 320/31.1#26.75#31.5#26.75



        try:

            #animalType = str(animalBox.bounding_boxes[0].Class)

            #CALCULATING
             #if class is one of these animals




                x_position = geometricBox.geometric_x# (x_max + x_min)/2 #calculate the pixel in optical frame [0-64]

                x_angle = x_position/angleScale-31.1#26.75#26.75
                x_angle = round(x_angle)

                if x_angle <0:

                    self.lidar_angle = int(-x_angle)
                else:
                    self.lidar_angle = int(359-x_angle)

                self.new_value = 1

                print(self.lidar_angle)

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
                self.get_hit()  ##When we have nu value we go into get_git function
                return #lidar_angle



        except (IndexError):
            return

        #TRANSLATE THIS TO ANGLE AROUND ROBOT
            #note: 53.5 degree viewing angle max (-26.75 to 26.75)
            #note: LaserScan (0-360) with 0 being in front, rotating CCW - base scan



    def callback2(self, laserData): #function for determining laser distance at determined angle
    #    print len(msg.ranges)

        self.ranges = laserData.ranges
        # if lidar_angle:
        #     print(lidar_angle)

        # try:
        #     animal_distance = laserData.ranges[lidar_angle]
        # # if x_angle:
        #     print(animal_distance)
        #
        # except(IndexError):
        #pub = rospy.Publisher('animalFound', Coordinates, queue_size=10)
        return

    def get_hit(self):
        pub = rospy.Publisher('Shape_info', geometricrelcoords, queue_size=10)

        animalDistance = self.ranges[self.lidar_angle]
        print(animalDistance)
        #x_cord = math.cosd(self.lidar_angle)*animalDistance
        #y_cord = math.sind(self.lidar_angle)*animalDistance
        geometric_coord_info = geometricrelcoords()

        x_cord = math.cos(math.radians(self.lidar_angle))*animalDistance
        y_cord = math.sin(math.radians(self.lidar_angle))*animalDistance
        #print(x_cord)
        #print(y_cord)
        #
        geometric_coord_info.geometricrel_x = x_cord #might be good for geometric
        geometric_coord_info.geometricrel_y = y_cord

        #
        try:
            pub.publish(geometric_coord_info)   #Publishing coordinates onto the "chatter" topic for the yaml file to read.

        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':

    lidar = lidar()

    #sub1 = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes , lidar.callback1)
    sub2 = rospy.Subscriber('/scan', LaserScan , lidar.callback2)
    sub3 = rospy.Subscriber('/shape/coordinates', geometricpixels , lidar.callback1)
    # sub3 = rospy.Subscriber('chatter', Coordinates , callback2)

    rospy.spin() #continuous loop
