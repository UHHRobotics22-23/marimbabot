cmake_minimum_required(VERSION 3.0.2)
project(marimbabot_simulation)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  src/detect_bar_contact.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)