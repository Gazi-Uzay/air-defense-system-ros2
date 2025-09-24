#ifndef MICRO_ROS_UTILS_H
#define MICRO_ROS_UTILS_H

#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rcl/rcl.h>

#include <hss_interfaces/msg/GimbalCmd.h>
#include <hss_interfaces/msg/GimbalFeedback.h>
#include <hss_interfaces/srv/FireCommand.h>

// Micro-ROS Globals (extern to be defined in main.cpp or micro_ros_utils.cpp)
extern rcl_publisher_t publisher_gimbal_feedback;
extern rcl_subscription_t subscriber_gimbal_cmd;
extern rcl_service_t service_fire_command;

extern hss_interfaces__msg__GimbalFeedback gimbal_feedback_msg;
extern hss_interfaces__msg__GimbalCmd gimbal_cmd_msg;
extern hss_interfaces__srv__FireCommand_Request fire_command_req;
extern hss_interfaces__srv__FireCommand_Response fire_command_res;

extern rclc_executor_t executor;
extern rcl_allocator_t allocator;
extern rcl_node_t node;
extern rcl_timer_t timer;

// Function Prototypes
void micro_ros_setup();
void timer_callback(rcl_timer_t * timer, int64_t last_call_time);
void gimbal_cmd_subscription_callback(const void * msgin);
void fire_command_service_callback(const void * request_msg, void * response_msg);

#endif // MICRO_ROS_UTILS_H
