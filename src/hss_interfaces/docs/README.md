# hss_interfaces Package

## Purpose
The `hss_interfaces` package defines the custom ROS 2 message (msg) and service (srv) types used for communication between different nodes within the HSS. This ensures a standardized and clear communication protocol across the entire system.

## Functionality
- **Custom Message Definitions:** Contains `.msg` files that define the structure of data exchanged between nodes. Examples include:
    - `GimbalCmd.msg`: For sending desired gimbal angles.
    - `GimbalFeedback.msg`: For receiving current gimbal angles and IMU data.
    - `Target.msg`: For conveying information about detected targets (ID, position, confidence, color).
    - `TargetArray.msg`: For publishing an array of detected targets.
- **Custom Service Definitions:** Contains `.srv` files that define request-response interactions between nodes. Examples include:
    - `FireCommand.srv`: For requesting a laser fire action.
    - `SetMode.srv`: For changing the operational mode of the system.
- **Inter-node Communication:** These definitions are crucial for enabling seamless and type-safe communication between all HSS components, from the vision system to the gimbal control and operation manager.
