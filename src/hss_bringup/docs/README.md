# hss_bringup Package

## Purpose
The `hss_bringup` package is responsible for launching and managing the various nodes and configurations required to start the entire HSS (Hava Savunma Sistemi) system or specific subsystems. It provides a centralized way to bring up the ROS 2 components in a coordinated manner.

## Functionality
- **Launch Files:** Contains ROS 2 launch files (e.g., `.launch.py` or `.launch.xml`) to start multiple nodes simultaneously.
- **Configuration Management:** Manages parameters and configurations for different nodes, ensuring proper system initialization.
- **System Integration:** Facilitates the integration and startup sequence of all HSS components, including vision, gimbal control, operation manager, and GUI.
- **Testing and Debugging:** Provides launch configurations for testing individual components or the entire system.
