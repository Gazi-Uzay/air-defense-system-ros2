# hss_gui Package

## Purpose
The `hss_gui` package provides the Ground Station Interface (GSI) for the HSS, offering a user-friendly way to monitor the system, control the gimbal manually, and manage engagement.

## Functionality
- **RTSP Video Stream Display:** Displays the real-time video feed from the system's camera via an RTSP stream.
- **Manual Gimbal Control:** Allows manual control of the gimbal using mouse movements on the video feed, publishing commands to the `/ui/mouse_target` topic.
- **Manual Engagement:** Provides an "FIRE" button for manual laser engagement in AUTO_TRACK and MANUAL_TRACK modes, triggering the `/laser/fire` command.
- **Telemetry Panel:** Displays critical system telemetry, including gimbal angles, active operational mode, target status (ID, position, confidence score, color), and QR code data.
- **Target Visualization:** Overlays detected target information (e.g., bounding boxes, color, QR code data) on the video stream.
- **Mode Selection:** Provides an interface to change the operational mode via the `/op/set_mode` service.
