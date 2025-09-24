# hss_gimbal_control Package

## Purpose
The `hss_gimbal_control` package provides the ROS 2 interface for controlling the gimbal. It acts as a bridge between the high-level ROS 2 system and the low-level gimbal firmware (ESP32).

## Functionality
- **Gimbal Command Subscription:** Subscribes to the `/gimbal/cmd` ROS 2 topic to receive desired gimbal angle commands from the operation manager or ground station.
- **Gimbal Feedback Publication:** Publishes the current gimbal position and IMU data to the `/gimbal/feedback` ROS 2 topic, received from the ESP32 firmware.
- **Communication with Firmware:** Translates ROS 2 commands into a format understandable by the ESP32 firmware and vice-versa, likely using micro-ROS or a serial communication interface.
- **Error Handling:** Implements basic error handling for communication with the gimbal firmware.
