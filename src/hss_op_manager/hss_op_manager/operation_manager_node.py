import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from hss_interfaces.msg import TargetArray
from hss_interfaces.msg import GimbalFeedback
from hss_interfaces.msg import GimbalCmd
from hss_interfaces.srv import SetMode
from hss_interfaces.srv import FireCommand

from std_msgs.msg import String # For /op/state
from geometry_msgs.msg import Point # Placeholder for /ui/mouse_target

class OperationManagerNode(Node):

    # Define operational modes
    MODE_AUTO_TRACK = "AUTO_TRACK"
    MODE_MANUAL_TRACK = "MANUAL_TRACK"
    MODE_AUTO_KILL_COLOR = "AUTO_KILL_COLOR"
    MODE_QR_ENGAGE = "QR_ENGAGE"
    MODE_SAFE = "SAFE"

    def __init__(self):
        super().__init__('operation_manager_node')

        # QoS Profile for reliable communication (commands, services)
        qos_profile_reliable = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        # QoS Profile for best effort communication (telemetry, vision data)
        qos_profile_best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=20
        )

        # Subscriptions
        self.target_subscription = self.create_subscription(
            TargetArray,
            '/vision/targets',
            self.target_callback,
            qos_profile_best_effort)
        self.gimbal_feedback_subscription = self.create_subscription(
            GimbalFeedback,
            '/gimbal/feedback',
            self.gimbal_feedback_callback,
            qos_profile_best_effort)
        self.mouse_target_subscription = self.create_subscription(
            Point, # Placeholder, will be defined in hss_gui
            '/ui/mouse_target',
            self.mouse_target_callback,
            qos_profile_best_effort)

        # Publishers
        self.gimbal_cmd_publisher = self.create_publisher(GimbalCmd, '/gimbal/cmd', qos_profile_reliable)
        self.op_state_publisher = self.create_publisher(String, '/op/state', qos_profile_reliable)
        # Laser fire command will be a service client or a publisher depending on final design
        # For now, let's make it a service client to FireCommand.srv
        self.laser_fire_client = self.create_client(FireCommand, '/laser/fire')
        while not self.laser_fire_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('laser_fire service not available, waiting again...')

        # Services
        self.set_mode_service = self.create_service(SetMode, '/op/set_mode', self.set_mode_callback)

        self.current_mode = self.MODE_SAFE
        self.op_state_publisher.publish(String(data=self.current_mode))
        self.get_logger().info(f'Operation Manager Node has been started in {self.current_mode} mode.')

        # Internal state variables
        self.last_gimbal_feedback = None
        self.last_target_array = None
        self.last_mouse_target = None

        # Timer for periodic tasks (e.g., mode logic, publishing gimbal commands)
        self.timer = self.create_timer(0.1, self.periodic_task) # 10 Hz

    def target_callback(self, msg):
        self.last_target_array = msg
        # self.get_logger().info(f'Received {len(msg.targets)} targets.')

    def gimbal_feedback_callback(self, msg):
        self.last_gimbal_feedback = msg
        # self.get_logger().info(f'Received gimbal feedback: Pan={msg.current_pan_angle:.2f}, Tilt={msg.current_tilt_angle:.2f}')

    def mouse_target_callback(self, msg):
        self.last_mouse_target = msg
        # self.get_logger().info(f'Received mouse target: X={msg.x:.2f}, Y={msg.y:.2f}')

    def set_mode_callback(self, request, response):
        if request.mode_name in [self.MODE_AUTO_TRACK, self.MODE_MANUAL_TRACK, self.MODE_AUTO_KILL_COLOR, self.MODE_QR_ENGAGE, self.MODE_SAFE]:
            self.current_mode = request.mode_name
            self.op_state_publisher.publish(String(data=self.current_mode))
            response.success = True
            self.get_logger().info(f'Mode changed to: {self.current_mode}')
        else:
            response.success = False
            self.get_logger().warn(f'Invalid mode requested: {request.mode_name}')
        return response

    def send_gimbal_command(self, pan_angle, tilt_angle):
        cmd_msg = GimbalCmd()
        cmd_msg.pan_angle = pan_angle
        cmd_msg.tilt_angle = tilt_angle
        self.gimbal_cmd_publisher.publish(cmd_msg)
        # self.get_logger().info(f'Published gimbal command: Pan={pan_angle:.2f}, Tilt={tilt_angle:.2f}')

    def send_laser_fire_command(self):
        if self.laser_fire_client.wait_for_service(timeout_sec=1.0):
            request = FireCommand.Request()
            request.fire_request = True
            future = self.laser_fire_client.call_async(request)
            # You might want to add a callback for the future to check the response
            self.get_logger().info('Sent laser fire command.')
        else:
            self.get_logger().warn('Laser fire service not available.')

    def periodic_task(self):
        # This is where the main operational logic for each mode will reside
        if self.current_mode == self.MODE_SAFE:
            # Gimbal parks, no movement, laser off
            self.send_gimbal_command(0.0, 0.0) # Park position
            pass
        elif self.current_mode == self.MODE_AUTO_TRACK:
            if self.last_target_array and len(self.last_target_array.targets) > 0:
                # Simple logic: track the first detected target
                target = self.last_target_array.targets[0]
                # For simulation, let's just command the gimbal to target's x,y position
                # In a real scenario, this would involve PID control to center the target
                self.send_gimbal_command(target.x_pos, target.y_pos) # Simplified
            else:
                self.get_logger().info('AUTO_TRACK: No targets detected.')
                self.send_gimbal_command(0.0, 0.0) # Return to center or last known position
        elif self.current_mode == self.MODE_MANUAL_TRACK:
            if self.last_mouse_target:
                # Command gimbal based on mouse input
                self.send_gimbal_command(self.last_mouse_target.x, self.last_mouse_target.y) # Simplified
            else:
                self.get_logger().info('MANUAL_TRACK: No mouse input.')
                self.send_gimbal_command(0.0, 0.0) # Return to center
        elif self.current_mode == self.MODE_AUTO_KILL_COLOR:
            if self.last_target_array and len(self.last_target_array.targets) > 0:
                # Find a red (enemy) target
                red_targets = [t for t in self.last_target_array.targets if t.color_info == "red"]
                if len(red_targets) > 0:
                    target = red_targets[0]
                    self.send_gimbal_command(target.x_pos, target.y_pos) # Track red target
                    # Simulate firing if target is centered (simplified)
                    if abs(target.x_pos) < 0.5 and abs(target.y_pos) < 0.5: # Assume centered if close to 0,0
                        self.send_laser_fire_command()
                else:
                    self.get_logger().info('AUTO_KILL_COLOR: No red targets detected.')
                    self.send_gimbal_command(0.0, 0.0)
            else:
                self.get_logger().info('AUTO_KILL_COLOR: No targets detected.')
                self.send_gimbal_command(0.0, 0.0)
        elif self.current_mode == self.MODE_QR_ENGAGE:
            if self.last_target_array and len(self.last_target_array.targets) > 0:
                # Find a target with QR code data
                qr_targets = [t for t in self.last_target_array.targets if t.qr_code_data != ""]
                if len(qr_targets) > 0:
                    target = qr_targets[0]
                    self.send_gimbal_command(target.x_pos, target.y_pos) # Track QR target
                    # Simulate firing if target is centered (simplified)
                    if abs(target.x_pos) < 0.5 and abs(target.y_pos) < 0.5: # Assume centered if close to 0,0
                        self.send_laser_fire_command()
                else:
                    self.get_logger().info('QR_ENGAGE: No QR targets detected.')
                    self.send_gimbal_command(0.0, 0.0)
            else:
                self.get_logger().info('QR_ENGAGE: No targets detected.')
                self.send_gimbal_command(0.0, 0.0)

def main(args=None):
    rclpy.init(args=args)
    operation_manager_node = OperationManagerNode()
    rclpy.spin(operation_manager_node)
    operation_manager_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
