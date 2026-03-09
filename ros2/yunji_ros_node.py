"""
Yunji Robot ROS Node - Runs on robot's ROS/ROS2 system

This version integrates with the robot's ROS ecosystem,
allowing for deeper control and sensor fusion.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
import json
import requests
from typing import Optional


class YunjiRosNode(Node):
    """
    ROS2 node for Yunji robot control.
    
    Publishes:
    - /robot_pose: Current robot pose
    - /cmd_vel: Velocity commands
    
    Subscribes:
    - /goal_pose: Navigation goal
    - /emergency_stop: Stop command
    """
    
    def __init__(self, robot_id: str, config: dict):
        super().__init__(yunji_{robot_id}')
        
        self.robot_id = robot_id
        self.config = config
        self.yunji_api_url = config.get('yunji_api_url', 'http://localhost:8080')
        
        # Publishers
        self.pose_pub = self.create_publisher(PoseStamped, '/robot_pose', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        
        # Subscribers
        self.goal_sub = self.create_subscription(
            PoseStamped, '/goal_pose', self.goal_callback, 10)
        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10)
            
        # Timer for status updates
        self.timer = self.create_timer(0.5, self.status_timer_callback)
        
        self.get_logger().info(f'Yunji ROS node started for {robot_id}')
        
    def goal_callback(self, msg: PoseStamped):
        """Handle navigation goal from ROS."""
        x = msg.pose.position.x
        y = msg.pose.position.y  # ROS uses Y, Yunji might use Z
        
        self.get_logger().info(f'Navigating to ({x}, {y})')
        
        # Send to Yunji API
        try:
            response = requests.post(
                f'{self.yunji_api_url}/api/navigation/move',
                json={
                    'target': {'position': {'x': x, 'y': 0, 'z': y}},
                    'options': {'speed': 0.5}
                },
                timeout=5
            )
            if response.status_code == 200:
                self.get_logger().info('Navigation command sent')
        except Exception as e:
            self.get_logger().error(f'Failed to send command: {e}')
            
    def cmd_callback(self, msg: Twist):
        """Handle velocity commands (direct control)."""
        # Direct velocity control if Yunji supports it
        pass
        
    def status_timer_callback(self):
        """Periodically get robot status and publish to ROS."""
        try:
            response = requests.get(
                f'{self.yunji_api_url}/api/status',
                timeout=2
            )
            if response.status_code == 200:
                status = response.json()
                self.publish_pose(status)
        except Exception as e:
            self.get_logger().warning(f'Status request failed: {e}')
            
    def publish_pose(self, status: dict):
        """Publish robot pose to ROS."""
        pos = status.get('position', {})
        
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        pose_msg.pose.position.x = pos.get('x', 0)
        pose_msg.pose.position.y = pos.get('z', 0)  # Map Z to Y
        pose_msg.pose.position.z = 0
        
        self.pose_pub.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)
    
    # Load config
    import yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    robot_id = config['yunji']['robot_ids'][0]  # Get first robot
    node = YunjiRosNode(robot_id, config)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
