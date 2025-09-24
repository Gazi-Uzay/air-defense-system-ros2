import rclpy
from rclpy.node import Node

from hss_interfaces.msg import Target
from hss_interfaces.msg import TargetArray

import random

class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')
        self.publisher_ = self.create_publisher(TargetArray, '/vision/targets', 10)
        self.timer = self.create_timer(1.0, self.publish_dummy_targets)  # Publish every 1 second
        self.get_logger().info('Vision Node has been started and is publishing dummy targets.')

        self.target_id_counter = 0

    def publish_dummy_targets(self):
        target_array_msg = TargetArray()
        
        # Simulate 1 to 3 targets
        num_targets = random.randint(1, 3)
        for _ in range(num_targets):
            target_msg = Target()
            self.target_id_counter += 1
            target_msg.id = self.target_id_counter
            target_msg.x_pos = float(random.uniform(-10.0, 10.0))
            target_msg.y_pos = float(random.uniform(-10.0, 10.0))
            target_msg.z_pos = float(random.uniform(0.0, 5.0))
            target_msg.confidence_score = float(random.uniform(0.7, 0.99))
            
            # Simulate color info
            colors = ["red", "blue", "none"]
            target_msg.color_info = random.choice(colors)

            # Simulate QR code data (only for some targets)
            if random.random() > 0.5:
                target_msg.qr_code_data = f"QR_{random.randint(1000, 9999)}"
            else:
                target_msg.qr_code_data = ""

            target_array_msg.targets.append(target_msg)
        
        self.publisher_.publish(target_array_msg)
        self.get_logger().info(f'Published {len(target_array_msg.targets)} dummy targets.')

def main(args=None):
    rclpy.init(args=args)
    vision_node = VisionNode()
    rclpy.spin(vision_node)
    vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
