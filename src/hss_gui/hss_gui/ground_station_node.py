import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from hss_interfaces.msg import GimbalFeedback, Target, TargetArray
from hss_interfaces.srv import SetMode, FireCommand

from std_msgs.msg import String
from geometry_msgs.msg import Point

import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

# --- Flask Web Server Setup ---
app = Flask(__name__, static_folder='www', static_url_path='')
CORS(app)
node_instance = None

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/state')
def get_state():
    if node_instance is None:
        return jsonify({"error": "Node not initialized"}), 500

    gimbal_feedback = {}
    if node_instance.current_gimbal_feedback:
        fb = node_instance.current_gimbal_feedback
        gimbal_feedback = {
            "pan": fb.current_pan_angle,
            "tilt": fb.current_tilt_angle
        }

    targets = []
    if node_instance.current_target_array:
        for t in node_instance.current_target_array.targets:
            targets.append({
                "id": t.id,
                "x": t.x,
                "y": t.y,
                "w": t.w,
                "h": t.h,
                "color": t.color
            })

    return jsonify({
        "op_state": node_instance.current_op_state,
        "gimbal_feedback": gimbal_feedback,
        "targets": targets
    })

@app.route('/api/set_mode', methods=['POST'])
def set_mode():
    mode_name = request.json.get('mode')
    if not mode_name or node_instance is None:
        return jsonify({"success": False, "message": "Invalid request"}), 400
    
    node_instance.call_set_mode_service(mode_name)
    return jsonify({"success": True, "message": f"Mode change requested to {mode_name}"})

@app.route('/api/fire', methods=['POST'])
def fire():
    if node_instance is None:
        return jsonify({"success": False, "message": "Node not initialized"}), 500

    node_instance.call_fire_command_service()
    return jsonify({"success": True, "message": "Fire command requested"})

@app.route('/api/mouse_target', methods=['POST'])
def mouse_target():
    data = request.json
    x = data.get('x')
    y = data.get('y')

    if x is None or y is None or node_instance is None:
        return jsonify({"success": False, "message": "Invalid coordinates"}), 400

    mouse_point = Point()
    mouse_point.x = float(x)
    mouse_point.y = float(y)
    mouse_point.z = 0.0
    node_instance.mouse_target_publisher.publish(mouse_point)
    return jsonify({"success": True})

# --- ROS 2 Node ---
class GroundStationNode(Node):

    def __init__(self):
        super().__init__('ground_station_node')

        # QoS Profiles
        qos_profile_reliable = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=10)
        qos_profile_best_effort = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=1)

        # Subscriptions
        self.create_subscription(GimbalFeedback, '/gimbal/feedback', self.gimbal_feedback_callback, qos_profile_best_effort)
        self.create_subscription(TargetArray, '/vision/targets', self.target_callback, qos_profile_best_effort)
        self.create_subscription(String, '/op/state', self.op_state_callback, qos_profile_reliable)

        # Publishers
        self.mouse_target_publisher = self.create_publisher(Point, '/ui/mouse_target', qos_profile_best_effort)

        # Service Clients
        self.set_mode_client = self.create_client(SetMode, '/op/set_mode')
        self.fire_command_client = self.create_client(FireCommand, '/laser/fire')
        
        self.get_logger().info("Checking for services...")
        if not self.set_mode_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('SetMode service not available.')
        if not self.fire_command_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('FireCommand service not available.')

        # Internal state variables
        self.current_gimbal_feedback = None
        self.current_target_array = None
        self.current_op_state = "UNKNOWN"

        self.get_logger().info('Ground Station Node has been started with web server.')

    def gimbal_feedback_callback(self, msg):
        self.current_gimbal_feedback = msg

    def target_callback(self, msg):
        self.current_target_array = msg

    def op_state_callback(self, msg):
        self.current_op_state = msg.data

    def call_set_mode_service(self, mode_name):
        if not self.set_mode_client.ready:
            self.get_logger().warn('SetMode service not ready.')
            return
        request = SetMode.Request()
        request.mode_name = mode_name
        future = self.set_mode_client.call_async(request)
        future.add_done_callback(self.service_response_callback)
        self.get_logger().info(f'Calling SetMode service with mode: {mode_name}')

    def call_fire_command_service(self):
        if not self.fire_command_client.ready:
            self.get_logger().warn('FireCommand service not ready.')
            return
        request = FireCommand.Request()
        request.fire_request = True
        future = self.fire_command_client.call_async(request)
        future.add_done_callback(self.service_response_callback)
        self.get_logger().info('Calling FireCommand service.')

    def service_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Service call successful: {response.success}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    global node_instance
    node_instance = GroundStationNode()

    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()

    try:
        rclpy.spin(node_instance)
    except KeyboardInterrupt:
        pass

    node_instance.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()