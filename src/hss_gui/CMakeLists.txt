cmake_minimum_required(VERSION 3.8)
project(hss_gui)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(hss_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_python_install_package(hss_gui)

ament_package()
