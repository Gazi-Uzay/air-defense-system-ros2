import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraPublisherNode(Node):
    def __init__(self):
        super().__init__('camera_publisher_node')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)  # 30 FPS
        self.bridge = CvBridge()
        self.width = 1280
        self.height = 720
        self.get_logger().info(f'Camera Publisher Node started. Publishing to /camera/image_raw at {self.width}x{self.height}')

    def timer_callback(self):
        # Create a black image
        img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Add text
        text = "SIMULATED CAMERA FEED"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (self.width - text_size[0]) // 2
        text_y = (self.height + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

        # Convert OpenCV image to ROS Image message
        ros_image = self.bridge.cv2_to_imgmsg(img, "bgr8")
        ros_image.header.stamp = self.get_clock().now().to_msg()
        ros_image.header.frame_id = "camera"
        
        self.publisher_.publish(ros_image)

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisherNode()
    rclpy.spin(camera_publisher)
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
