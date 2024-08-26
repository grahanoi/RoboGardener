cmake_minimum_required(VERSION 3.5)
project(RoboGardener)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(urdf REQUIRED)
find_package(robot_state_publisher REQUIRED)

# Install directories
install(DIRECTORY launch urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
