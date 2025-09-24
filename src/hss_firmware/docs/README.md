# hss_firmware Package

## Purpose
The `hss_firmware` package contains the embedded software (firmware) for the ESP32 microcontroller, which is responsible for low-level hardware control and interaction within the HSS.

## Functionality
- **Gimbal PID Control:** Implements the PID control loop for the step motors to precisely control the gimbal's pan and tilt angles at a high frequency (>= 500 Hz).
- **IMU Data Acquisition:** Reads and processes data from the integrated IMU sensor to provide accurate gimbal orientation and feedback.
- **Button and Kill Switch Handling:** Monitors physical buttons and the kill switch connected to the ESP32 for mode changes and emergency stops.
- **Laser Firing Control:** Manages the activation and deactivation of the laser engagement mechanism based on commands received.
- **micro-ROS Integration:** Publishes gimbal feedback (angle, IMU data) and button states, and subscribes to gimbal commands and laser fire commands via micro-ROS topics.
- **Limit Switch Management:** Handles limit switch inputs for safe parking and homing of the gimbal.
