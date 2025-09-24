import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from hss_interfaces.msg import GimbalFeedback
from hss_interfaces.msg import TargetArray
from hss_interfaces.srv import SetMode
from hss_interfaces.srv import FireCommand

from std_msgs.msg import String
from geometry_msgs.msg import Point

import random

class GroundStationNode(Node):

    def __init__(self):
        super().__init__('ground_station_node')

        # QoS Profile for reliable communication
        qos_profile_reliable = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        # QoS Profile for best effort communication
        qos_profile_best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=20
        )

        # Subscriptions
        self.gimbal_feedback_subscription = self.create_subscription(
            GimbalFeedback,
            '/gimbal/feedback',
            self.gimbal_feedback_callback,
            qos_profile_best_effort)
        self.target_subscription = self.create_subscription(
            TargetArray,
            '/vision/targets',
            self.target_callback,
            qos_profile_best_effort)
        self.op_state_subscription = self.create_subscription(
            String,
            '/op/state',
            self.op_state_callback,
            qos_profile_reliable)

        # Publishers
        self.mouse_target_publisher = self.create_publisher(Point, '/ui/mouse_target', qos_profile_best_effort)

        # Service Clients
        self.set_mode_client = self.create_client(SetMode, '/op/set_mode')
        while not self.set_mode_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('set_mode service not available, waiting again...')

        self.fire_command_client = self.create_client(FireCommand, '/laser/fire')
        while not self.fire_command_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('fire_command service not available, waiting again...')

        self.get_logger().info('Ground Station Node has been started.')

        # Internal state variables
        self.current_gimbal_feedback = None
        self.current_target_array = None
        self.current_op_state = "UNKNOWN"

        # Timers for simulating GUI interactions
        self.mouse_timer = self.create_timer(0.5, self.publish_dummy_mouse_target) # Simulate mouse movement
        self.mode_change_timer = self.create_timer(5.0, self.cycle_modes) # Simulate mode changes
        self.fire_timer = self.create_timer(10.0, self.simulate_fire_command) # Simulate fire command

        self.modes = ["AUTO_TRACK", "MANUAL_TRACK", "AUTO_KILL_COLOR", "QR_ENGAGE", "SAFE"]
        self.mode_index = 0

    def gimbal_feedback_callback(self, msg):
        self.current_gimbal_feedback = msg
        # self.get_logger().info(f'GUI: Received gimbal feedback: Pan={msg.current_pan_angle:.2f}, Tilt={msg.current_tilt_angle:.2f}')

    def target_callback(self, msg):
        self.current_target_array = msg
        # self.get_logger().info(f'GUI: Received {len(msg.targets)} targets.')

    def op_state_callback(self, msg):
        self.current_op_state = msg.data
        self.get_logger().info(f'GUI: Current operational mode: {self.current_op_state}')

    def publish_dummy_mouse_target(self):
        mouse_point = Point()
        mouse_point.x = float(random.uniform(-1.0, 1.0))
        mouse_point.y = float(random.uniform(-1.0, 1.0))
        mouse_point.z = 0.0 # Not used for 2D mouse input
        self.mouse_target_publisher.publish(mouse_point)
        # self.get_logger().info(f'GUI: Published dummy mouse target: X={mouse_point.x:.2f}, Y={mouse_point.y:.2f}')

    def cycle_modes(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        next_mode = self.modes[self.mode_index]
        self.call_set_mode_service(next_mode)

    def call_set_mode_service(self, mode_name):
        request = SetMode.Request()
        request.mode_name = mode_name
        future = self.set_mode_client.call_async(request)
        future.add_done_callback(self.set_mode_response_callback)
        self.get_logger().info(f'GUI: Calling SetMode service with mode: {mode_name}')

    def set_mode_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'GUI: Successfully changed mode.')
            else:
                self.get_logger().warn(f'GUI: Failed to change mode.')
        except Exception as e:
            self.get_logger().error(f'GUI: Service call failed: {e}')

    def simulate_fire_command(self):
        if self.current_op_state in ["AUTO_TRACK", "MANUAL_TRACK"]:
            self.call_fire_command_service()
        else:
            self.get_logger().info(f'GUI: Not firing in {self.current_op_state} mode.')

    def call_fire_command_service(self):
        request = FireCommand.Request()
        request.fire_request = True
        future = self.fire_command_client.call_async(request)
        future.add_done_callback(self.fire_command_response_callback)
        self.get_logger().info('GUI: Calling FireCommand service.')

    def fire_command_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'GUI: Fire command successful.')
            else:
                self.get_logger().warn(f'GUI: Fire command failed.')
        except Exception as e:
            self.get_logger().error(f'GUI: Fire command service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    ground_station_node = GroundStationNode()
    rclpy.spin(ground_station_node)
    ground_station_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
