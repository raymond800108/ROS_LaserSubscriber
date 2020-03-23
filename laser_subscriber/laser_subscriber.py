#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist # Import twist messages for velocity control
from sensor_msgs.msg import LaserScan # Import LaserScan to read values

left = 0
straight = 0
right = 0
def callback(msg):
    global left
    global straight
    global right
    right = msg.ranges[260]
    straight = msg.ranges[360]
    left = msg.ranges[460]
    print("Left: " , left)
    print("Right: ", right)
    print("Straight", straight)

rospy.init_node('Topic_quiz_node')
sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback)

#Make the robot move
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
move = Twist()

while not rospy.is_shutdown():
    if left > 1.5 and straight > 1.5 and right > 1.5: # no object detected
        move.linear.x = 0.5
        move.angular.z = 0
    else: # object detected
        move.linear.x = 0
        move.angular.z = 0.5

    pub.publish(move)  # puplish to topic in order to move the robot
    rate.sleep()       # sleep to keep rate at 2 hz