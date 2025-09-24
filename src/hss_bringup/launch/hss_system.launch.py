from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hss_gimbal_control',
            executable='gimbal_control_node',
            name='gimbal_control_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='hss_vision',
            executable='vision_node',
            name='vision_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='hss_op_manager',
            executable='operation_manager_node',
            name='operation_manager_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            package='hss_gui',
            executable='ground_station_node',
            name='ground_station_node',
            output='screen',
            emulate_tty=True,
        ),
    ])
