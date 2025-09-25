import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

from hss_interfaces.msg import Target, TargetArray

import random

class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')
        self.target_publisher_ = self.create_publisher(TargetArray, '/vision/targets', 10)
        self.image_publisher_ = self.create_publisher(Image, '/vision/image_processed', 10)
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        self.bridge = CvBridge()
        self.get_logger().info('Vision Node has been started and is subscribed to /camera/image_raw.')

        self.target_id_counter = 0

    def image_callback(self, msg):
        self.get_logger().debug('Received image, processing for dummy targets...')
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return

        target_array_msg = TargetArray()
        
        # Simulate finding targets and draw them on the image
        num_targets = random.randint(1, 3)
        for _ in range(num_targets):
            target_msg = Target()
            self.target_id_counter += 1
            target_msg.id = self.target_id_counter
            target_msg.x_pos = float(random.uniform(-10.0, 10.0))
            target_msg.y_pos = float(random.uniform(-10.0, 10.0))
            target_msg.z_pos = float(random.uniform(0.0, 5.0))
            target_msg.confidence_score = float(random.uniform(0.7, 0.99))
            colors = ["red", "blue", "none"]
            target_msg.color_info = random.choice(colors)
            if random.random() > 0.5:
                target_msg.qr_code_data = f"QR_{random.randint(1000, 9999)}"
            else:
                target_msg.qr_code_data = ""
            target_array_msg.targets.append(target_msg)

            # Draw a bounding box for the simulated target
            h, w, _ = cv_image.shape
            pt1 = (random.randint(0, w - 100), random.randint(0, h - 100))
            pt2 = (pt1[0] + random.randint(20, 100), pt1[1] + random.randint(20, 100))
            color_map = {"red": (0, 0, 255), "blue": (255, 0, 0), "none": (0, 255, 0)}
            bgr_color = color_map.get(target_msg.color_info, (0, 255, 0))
            cv2.rectangle(cv_image, pt1, pt2, bgr_color, 2)
            cv2.putText(cv_image, f"ID: {target_msg.id}", (pt1[0], pt1[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, bgr_color, 2)

        # Publish the target data
        self.target_publisher_.publish(target_array_msg)
        self.get_logger().info(f'Published {len(target_array_msg.targets)} dummy targets.')

        # Publish the processed image
        try:
            processed_image_msg = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
            processed_image_msg.header = msg.header
            self.image_publisher_.publish(processed_image_msg)
        except Exception as e:
            self.get_logger().error(f'Failed to convert and publish processed image: {e}')

def main(args=None):
    rclpy.init(args=args)
    vision_node = VisionNode()
    rclpy.spin(vision_node)
    vision_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
