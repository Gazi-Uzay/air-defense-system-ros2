cmake_minimum_required(VERSION 3.8)
project(hss_gimbal_control)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(hss_interfaces REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_python_install_package(hss_gimbal_control)

ament_package()
