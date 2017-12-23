#!/usr/bin/env python
import os, sys, rospy, tf, actionlib, moveit_commander
from control_msgs.msg import (GripperCommandAction, GripperCommandGoal)
from geometry_msgs.msg import *
from tf.transformations import quaternion_from_euler, euler_from_quaternion

if __name__ == '__main__':
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('pick_up_item')
#   args = rospy.myargv(argv = sys.argv)
#   if len(args) != 2:
#     print("usage: pick_up_item.py BIN_NUMBER")
#     sys.exit(1)
#   item_frame = "item_{0}".format(int(args[1]))

#   gripper = actionlib.SimpleActionClient("gripper_controller/gripper_action",
#     GripperCommandAction)
#   gripper.wait_for_server() # <1>

  arm = moveit_commander.MoveGroupCommander("onine_arm") # <2>
  arm.allow_replanning(True)
  tf_listener = tf.TransformListener() # <3>
  rate = rospy.Rate(10)

#   gripper_goal = GripperCommandGoal() # <4>
#   gripper_goal.command.max_effort = 10.0

#   p = Pose()
#   p.position.x = 0.4
#   p.position.z = 0.7
#   p.orientation = Quaternion(*quaternion_from_euler(0, 1, 1))
#   arm.set_pose_target(p) # <5>
#   arm.go(True)

#   os.system("./look_at_bin.py") # <6>
  p = Pose()
# 1.7299215079
# [0.007533234163447561, 0.2361223818537537, 0.46681790857795324]
# item: [0.007533234163447561, 0.2361223818537537, 0.46681790857795324]

  while not rospy.is_shutdown():
    rate.sleep()
    # try:
    #   t = tf_listener.getLatestCommonTime('/braccio_base_link', '/ar_marker_3') # <7>
    #   if (rospy.Time.now() - t).to_sec() > 0.2:
    #     rospy.sleep(0.1)
    #     continue

    #   (item_translation, item_orientation) = tf_listener.lookupTransform('/braccio_base_link', "ar_marker_3", t) # <8>
    # except(tf.Exception, tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #     continue

    
    # (roll,pitch,yaw) = euler_from_quaternion(item_orientation)
    # print yaw
    
    # try:
    #   t = tf_listener.getLatestCommonTime('/base_footprint', '/ar_marker_3') # <7>
    #   if (rospy.Time.now() - t).to_sec() > 0.2:
    #     rospy.sleep(0.1)
    #     continue

    #   (item_translation, item_orientation) = tf_listener.lookupTransform('/base_footprint', "ar_marker_3", t) # <8>
    # except(tf.Exception, tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #     continue
    # print item_translation

    try:
      t = tf_listener.getLatestCommonTime('/base_footprint', '/wrist_roll_link') # <7>
      if (rospy.Time.now() - t).to_sec() > 0.2:
        rospy.sleep(0.1)
        continue

      (item_translation, item_orientation) = tf_listener.lookupTransform('/base_footprint', "/wrist_roll_link", t) # <8>
    except(tf.Exception, tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue
    print item_translation
    (roll,pitch,yaw) = euler_from_quaternion(item_orientation)
    print "converted"
    print roll
    print pitch
    print yaw
    print item_translation

    yaw = -1.67922115693
    item_translation = [0.39568175951513196, -0.032457596310244946, 0.6319669783583116]




    # yaw = 1.73645785256 - 3.1416
    # item_translation = [0.3227387180770045, -0.04783483011548259, 0.7819707036138221]

    print("item: " + str(item_translation))
    p.position.x = item_translation[0] - 0.01
    p.position.y = item_translation[1] 
    p.position.z = item_translation[2] 
    p.orientation = Quaternion(*quaternion_from_euler(-1.55961170956, 0.00000, yaw))
    # print("RANDOM")
    # print(arm.get_random_pose())

    arm.set_pose_target(p)
    arm.set_goal_tolerance(0.005)
    # # arm.set_goal_position_tolerance(0.05)
    # arm.set_goal_orientation_tolerance(0.1)
    arm.set_num_planning_attempts(100)
    arm.set_planning_time(10)
    arm.set_planner_id("RRTkConfigDefault")
    # arm.go(True) # <10>

    plan1 = arm.plan()

    arm.execute(plan1)

   
    # gripper_goal.command.position = 0
    # gripper.send_goal(gripper_goal)
    # gripper.wait_for_result(rospy.Duration(2.0))

    # p.position.x = 0.05
    # p.position.y = -0.15
    # p.position.z = 0.75
    # p.orientation = Quaternion(*quaternion_from_euler(0, -1.5, -1.5))
    # arm.set_pose_target(p)
    # arm.go(True) # <12>
    break # <13>