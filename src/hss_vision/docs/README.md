# hss_vision Package

## Purpose
The `hss_vision` package is responsible for all image processing and computer vision tasks within the HSS, including target detection, tracking, classification, and QR code recognition.

## Functionality
- **Camera Feed Processing:** Acquires and processes video frames from a ROS 2 topic (`/camera/image_raw`).
- **Target Detection and Tracking:** Implements algorithms (e.g., OpenCV, YOLO, TensorRT) to detect and track moving targets within the camera's field of view at >= 15 FPS.
- **Color Separation (Stage 2):** Identifies and differentiates targets based on color (red for enemy, blue for friendly) for autonomous engagement in `AUTO_KILL_COLOR` mode.
- **QR Code Detection (Stage 3):** Detects and decodes QR codes displayed at the weapon's zero point for target engagement in `QR_ENGAGE` mode.
- **Target Information Extraction:** For each detected target, extracts and calculates relevant information such as ID, position, confidence score, and color (if applicable).
- **Target Data Publication:** Publishes the processed target information, including QR code data, to the `/vision/targets` ROS 2 topic.
- **RTSP Stream Generation:** Potentially responsible for generating the RTSP video stream for the ground station interface.

## Nodes

### `vision_node.py`
- **Purpose:** The main node for processing camera frames and performing target detection.
- **Subscribes to:** `/camera/image_raw` (sensor_msgs/msg/Image)
- **Publishes to:** `/vision/targets` (hss_interfaces/msg/TargetArray)
- **Description:** This node receives raw image data, applies vision algorithms to detect targets, and publishes the results for the `hss_op_manager` to use.

### `camera_publisher_node.py`
- **Purpose:** A simulated camera publisher for development and testing.
- **Publishes to:** `/camera/image_raw` (sensor_msgs/msg/Image)
- **Description:** This node generates a black screen with "SIMULATED CAMERA FEED" text and publishes it at 30 FPS. It allows for testing the vision pipeline without a physical camera attached.
