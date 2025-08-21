#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Quaternion
import tf
import numpy as np

class OdometryConverter:
    def __init__(self):
        self.namespace = rospy.get_namespace().replace('/', '')
        rospy.loginfo('Initialize enu to ned for vehicle <%s>' % self.namespace)

        # Publisher for NED odometry
        self.odom_ned_pub = rospy.Publisher('pose_gt_ned', Odometry, queue_size=10)

        # Subscriber to ENU odometry
        rospy.Subscriber('odom', Odometry, self.odom_callback)

        

    def odom_callback(self, msg):
        # Create a new Odometry message for NED
        odom_ned = Odometry()
        odom_ned.header = msg.header
        odom_ned.header.frame_id = "world_ned" # Set the new frame ID

        # Convert position from ENU to NED
        # ENU: x_e, y_n, z_u
        # NED: x_n, y_e, z_d
        # So: x_ned = y_enu, y_ned = x_enu, z_ned = -z_enu
        odom_ned.pose.pose.position.x = msg.pose.pose.position.y
        odom_ned.pose.pose.position.y = msg.pose.pose.position.x
        odom_ned.pose.pose.position.z = -msg.pose.pose.position.z

        # Convert orientation from ENU to NED
        # This involves a rotation about the Z-axis by -90 degrees (or +270)
        # followed by a rotation about the new X-axis by 180 degrees.
        # Alternatively, a direct transformation matrix can be used.
        
        # Get quaternion from ENU odometry
        q_enu = [msg.pose.pose.orientation.x,
                 msg.pose.pose.orientation.y,
                 msg.pose.pose.orientation.z,
                 msg.pose.pose.orientation.w]

        # Define the rotation from ENU to NED as a quaternion
        # This is a rotation of 90 degrees around Z (ENU) then 180 around X (new frame)
        # Equivalent to rotating ENU's X to NED's Y, ENU's Y to NED's X, ENU's Z to NED's -Z
        q_enu_to_ned = tf.transformations.quaternion_from_euler(np.pi, 0, np.pi/2) # Roll 180, Yaw 90

        # Multiply the quaternions to get the new orientation
        q_ned = tf.transformations.quaternion_multiply(q_enu_to_ned, q_enu)

        odom_ned.pose.pose.orientation = Quaternion(*q_ned)

        # Copy covariance (assuming it's valid across frame transformations, or re-calculate if needed)
        odom_ned.pose.covariance = msg.pose.covariance

        # Copy twist information (linear and angular velocities)
        # These also need to be transformed if they are in the robot's body frame
        # and not already expressed in the world_enu frame.
        # For simplicity, assuming velocities are also transformed similarly to position.
        odom_ned.twist.twist.linear.x = msg.twist.twist.linear.y
        odom_ned.twist.twist.linear.y = msg.twist.twist.linear.x
        odom_ned.twist.twist.linear.z = -msg.twist.twist.linear.z

        # Angular velocities need similar rotation
        odom_ned.twist.twist.angular.x = msg.twist.twist.angular.y
        odom_ned.twist.twist.angular.y = msg.twist.twist.angular.x
        odom_ned.twist.twist.angular.z = -msg.twist.twist.angular.z

        odom_ned.twist.covariance = msg.twist.covariance

        # Publish the NED odometry
        self.odom_ned_pub.publish(odom_ned)

if __name__ == '__main__':
    print('Starting odometry converter')
    rospy.init_node('starting odometry converter')
    try:
        OdometryConverter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass