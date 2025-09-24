#include "micro_ros_utils.h"
#include "gimbal_controller.h" // For target_pan_angle, target_tilt_angle
#include "hardware_interface.h" // For set_laser_state

#include <micro_ros_platformio.h>
#include <rcl/error_handling.h>

// Micro-ROS Globals (defined here)
rcl_publisher_t publisher_gimbal_feedback;
rcl_subscription_t subscriber_gimbal_cmd;
rcl_service_t service_fire_command;

hss_interfaces__msg__GimbalFeedback gimbal_feedback_msg;
hss_interfaces__msg__GimbalCmd gimbal_cmd_msg;
hss_interfaces__srv__FireCommand_Request fire_command_req;
hss_interfaces__srv__FireCommand_Response fire_command_res;

rclc_executor_t executor;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

void micro_ros_setup() {
  allocator = rcl_get_default_allocator();

  // create init_options
  rcl_init_options_t init_options = rcl_get_zero_initialized_init_options();
  rcl_init_options_init(&init_options, allocator);
  rcl_init_options_set_domain_id(&init_options, 0); // Default domain ID

  // create node
  rclc_support_t support;
  rclc_support_init(&support, 0, NULL, &init_options, allocator);
  rclc_node_init_default(&node, "esp32_gimbal_node", "", &support);

  // create publisher for gimbal feedback
  rclc_publisher_init_default(
    &publisher_gimbal_feedback,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(hss_interfaces, msg, GimbalFeedback),
    "/gimbal/feedback");

  // create subscriber for gimbal command
  rclc_subscription_init_default(
    &subscriber_gimbal_cmd,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(hss_interfaces, msg, GimbalCmd),
    "/gimbal/cmd");

  // create service for fire command
  rclc_service_init_default(
    &service_fire_command,
    &node,
    ROSIDL_GET_SRV_TYPE_SUPPORT(hss_interfaces, srv, FireCommand),
    "/laser/fire");

  // create timer for publishing feedback (e.g., 100ms)
  rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(100),
    timer_callback);

  // create executor
  rclc_executor_init(&executor, &support, 3, &allocator);
  rclc_executor_add_timer(&executor, &timer);
  rclc_executor_add_subscription(&executor, &subscriber_gimbal_cmd, &gimbal_cmd_msg, &gimbal_cmd_subscription_callback, ON_NEW_DATA);
  rclc_executor_add_service(&executor, &service_fire_command, &fire_command_req, &fire_command_res, &fire_command_service_callback);
}

// --- Callbacks ---
void timer_callback(rcl_timer_t * timer, int64_t last_call_time) {
  RCLC_UNUSED(last_call_time);
  if (timer != NULL) {
    // Publish gimbal feedback
    gimbal_feedback_msg.current_pan_angle = current_pan_angle;
    gimbal_feedback_msg.current_tilt_angle = current_tilt_angle;
    // Placeholder IMU data
    gimbal_feedback_msg.imu_roll = imu_roll;
    gimbal_feedback_msg.imu_pitch = imu_pitch;
    gimbal_feedback_msg.imu_yaw = imu_yaw;
    rcl_publish(&publisher_gimbal_feedback, &gimbal_feedback_msg, NULL);
  }
}

void gimbal_cmd_subscription_callback(const void * msgin) {
  const hss_interfaces__msg__GimbalCmd * msg = (const hss_interfaces__msg__GimbalCmd *)msgin;
  target_pan_angle = msg->pan_angle;
  target_tilt_angle = msg->tilt_angle;
  Serial.printf("Received Gimbal Command: Pan=%.2f, Tilt=%.2f\n", target_pan_angle, target_tilt_angle);
}

void fire_command_service_callback(const void * request_msg, void * response_msg) {
  hss_interfaces__srv__FireCommand_Request * req = (hss_interfaces__srv__FireCommand_Request *)request_msg;
  hss_interfaces__srv__FireCommand_Response * res = (hss_interfaces__srv__FireCommand_Response *)response_msg;

  if (req->fire_request) {
    Serial.println("Received Fire Command Request: Activating Laser!");
    set_laser_state(true);
    delay(100); // Laser on for 100ms
    set_laser_state(false);
    res->success = true;
  } else {
    Serial.println("Received Fire Command Request: No action (fire_request is false).");
    res->success = false;
  }
}
