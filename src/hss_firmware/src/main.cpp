#include <Arduino.h>
#include <micro_ros_platformio.h>

#include "gimbal_controller.h"
#include "sensor_reader.h"
#include "hardware_interface.h"
#include "micro_ros_utils.h"

// --- Setup --- 
void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);

  initialize_hardware_pins();

  // IMU Setup (Placeholder)
  // if (!mpu.begin()) {
  //   Serial.println("Failed to find MPU6050 chip");
  //   while (1) { delay(10); }
  // }
  // mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  // mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  // mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(2000); // Wait for micro-ROS agent
  micro_ros_setup();
}

// --- Loop --- 
void loop() {
  RCLC_EXECUTE_EVERY_MS(10, rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10)));

  // Read sensors and update gimbal state at a high frequency (e.g., 500Hz)
  read_imu_data();
  read_buttons_and_switches();
  update_gimbal_pid();

  // Move steppers based on PID output
  move_stepper(PAN_STEP_PIN, PAN_DIR_PIN, current_pan_angle, target_pan_angle);
  move_stepper(TILT_STEP_PIN, TILT_DIR_PIN, current_tilt_angle, target_tilt_angle);
}