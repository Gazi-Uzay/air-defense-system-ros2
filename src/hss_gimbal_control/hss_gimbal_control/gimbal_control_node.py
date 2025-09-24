import rclpy
from rclpy.node import Node

from hss_interfaces.msg import GimbalCmd
from hss_interfaces.msg import GimbalFeedback

class GimbalControlNode(Node):

    def __init__(self):
        super().__init__('gimbal_control_node')
        self.subscription = self.create_subscription(
            GimbalCmd,
            '/gimbal/cmd',
            self.gimbal_cmd_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(GimbalFeedback, '/gimbal/feedback', 10)
        self.get_logger().info('Gimbal Control Node has been started.')

        # Simulate current gimbal state
        self.current_pan_angle = 0.0
        self.current_tilt_angle = 0.0
        self.imu_roll = 0.0
        self.imu_pitch = 0.0
        self.imu_yaw = 0.0

    def gimbal_cmd_callback(self, msg):
        self.get_logger().info(f'Received Gimbal Command: Pan={msg.pan_angle:.2f}, Tilt={msg.tilt_angle:.2f}')

        # Simulate gimbal movement and update current state
        self.current_pan_angle = msg.pan_angle
        self.current_tilt_angle = msg.tilt_angle
        # Simulate some IMU data change
        self.imu_roll += 0.01
        self.imu_pitch += 0.005
        self.imu_yaw += 0.001

        # Publish feedback
        feedback_msg = GimbalFeedback()
        feedback_msg.current_pan_angle = self.current_pan_angle
        feedback_msg.current_tilt_angle = self.current_tilt_angle
        feedback_msg.imu_roll = self.imu_roll
        feedback_msg.imu_pitch = self.imu_pitch
        feedback_msg.imu_yaw = self.imu_yaw
        self.publisher_.publish(feedback_msg)
        self.get_logger().info(f'Published Gimbal Feedback: Pan={feedback_msg.current_pan_angle:.2f}, Tilt={feedback_msg.current_tilt_angle:.2f}')


def main(args=None):
    rclpy.init(args=args)
    gimbal_control_node = GimbalControlNode()
    rclpy.spin(gimbal_control_node)
    gimbal_control_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
