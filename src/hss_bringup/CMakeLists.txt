cmake_minimum_required(VERSION 3.8)
project(hss_bringup)

find_package(ament_cmake REQUIRED)
find_package(launch_ros REQUIRED)
find_package(launch REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_python_install_package(hss_bringup)

ament_package()
