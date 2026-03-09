from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Yunji robot driver
        Node(
            package='yunji_ros_driver',
            executable='yunji_node',
            name='yunji_driver',
            parameters=[{
                'robot_id': 'robot_001',
                'yunji_api_url': 'http://localhost:8080'
            }]
        ),
        
        # PoseMesh sensor integration
        Node(
            package='yunji_ros_driver',
            executable='posemesh_sensor',
            name='posemesh_sensor',
            parameters=[{
                'domain_id': 'retail-store-01',
                'hagall_url': 'ws://localhost:8080',
                'participant_id': 'robot_001'
            }]
        ),
    ])
