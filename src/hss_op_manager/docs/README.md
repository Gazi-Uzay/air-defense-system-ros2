# hss_op_manager Package

## Purpose
The `hss_op_manager` package serves as the central operational manager for the HSS, orchestrating the system's behavior based on different operational modes, vision data, and user inputs.

## Functionality
- **Mode Management:** Manages the five operational modes: `AUTO_TRACK`, `MANUAL_TRACK`, `AUTO_KILL_COLOR`, `QR_ENGAGE`, and `SAFE`.
- **Mode Transition:** Handles transitions between modes based on physical button inputs or requests via the `/op/set_mode` service.
- **Gimbal Command Generation:** In `AUTO_TRACK` and `AUTO_KILL_COLOR` modes, processes target data from `/vision/targets` to generate and publish `/gimbal/cmd` messages to keep the target centered. In `MANUAL_TRACK` mode, it processes `/ui/mouse_target` data to generate gimbal commands.
- **Laser Engagement Logic:** In `AUTO_KILL_COLOR` and `QR_ENGAGE` modes, autonomously triggers laser firing via the `/laser/fire` command based on target detection and criteria. In other modes, it relays manual fire commands from the GUI.
- **State Publication:** Publishes the current operational mode to the `/op/state` topic for monitoring by the GUI and other nodes.
- **Failsafe Integration:** Interacts with failsafe mechanisms, potentially transitioning to `SAFE` mode upon critical events (e.g., loss of command, kill switch activation).
- **Target Processing:** Subscribes to `/vision/targets` to receive and interpret target information, including color and QR code data, for decision-making in various modes.
