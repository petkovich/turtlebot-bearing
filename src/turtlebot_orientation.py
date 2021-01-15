#!/usr/bin/env python  
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf
import numpy as np
from utils import *

class TurtlebotOrientation():
    def __init__(self):
        rospy.init_node('turlebot_orientation', anonymous=True)                                                     
        self.publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.laser_subscriber = rospy.Subscriber('/scan',LaserScan, self.laser_callback)
        self.odom_subscriber = rospy.Subscriber('/odom',Odometry, self.odom_callback)
        self.ranges = None
        self.odom = None
        self.orientation = None
        self.angle_min = None
        self.angle_max = None
        self.angle_increment = None
        self.range_max = None
        self.angle_indices = None
    def laser_callback(self, scan):
        self.ranges = scan.ranges
        self.angle_min = scan.angle_min
        self.angle_max = scan.angle_max
        self.angle_increment = scan.angle_increment
        self.angle_indices = np.arange(self.angle_min,self.angle_max + self.angle_increment,
                                       self.angle_increment) #added increment for endpoint
    def odom_callback(self, odom):
        self.odom = odom

    def controller(self):   
        if self.odom is not None: #if I know my orientation
            euler_orientation = tf.transformations.euler_from_quaternion((self.odom.pose.pose.orientation.x,
                                                                          self.odom.pose.pose.orientation.y,
                                                                          self.odom.pose.pose.orientation.z,
                                                                          self.odom.pose.pose.orientation.w))
            my_orientation = euler_orientation[2] #XY plane orientation (bearing)
            if self.ranges is not None: #if I have scan
                if min(self.ranges) < range_threshold: #if I am close enough
                    wanted_bearing = self.angle_indices[np.argmin(self.ranges)]
                    control_input = (-wanted_bearing + pi) % (2 * pi) - pi # min scan orientation -pi to pi
                    rospy.loginfo("I am close enough, turning for %f", control_input)
                else:
                    control_input = anglediff(default_bearing, my_orientation) #go to default bearing
                    rospy.loginfo("I am not close enough, turning to %f", default_bearing)
            else:
                control_input = anglediff(default_bearing, my_orientation)  #go to default bearing
                rospy.loginfo("Did not receive scan, turning to %f", default_bearing)

            if abs(control_input) < control_min_threshold: #don't move if close enough
                control_input = 0.0
            if abs(control_input) > control_max_threshold: #don't move too fast
                control_input = control_max_threshold * abs(control_input)/control_input    
            control_velocity = -control_input #inverted Z axis on the turtlebot
            published_velocity = Twist()
            published_velocity.angular.z = control_velocity
            self.publisher.publish(published_velocity) #publish velocity
        else:
            rospy.loginfo("Did not receive odometry.")

    def run(self):
        my_rate = rospy.Rate(controller_rate)
        while not rospy.is_shutdown():
            self.controller()
            my_rate.sleep() 


if __name__ == '__main__':
    my_turtlebot = TurtlebotOrientation()  
    try:
        my_turtlebot.run()
    except rospy.ROSInterruptException:
        pass
