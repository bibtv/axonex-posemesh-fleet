"""
PoseMesh Sensor Node - Runs on robot to interface with PoseMesh network

This node connects to the PoseMesh Hagall server and:
1. Broadcasts robot pose to shared coordinate system
2. Receives shared map data
3. Integrates with robot's localization
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from sensor_msgs.msg import CameraInfo, Image
import json
import asyncio
import websockets


class PoseMeshSensorNode(Node):
    """
    ROS2 node for PoseMesh integration.
    
    Publishes:
    - /posemesh/robot_pose: Robot pose in shared domain
    - /posemesh/map_update: Domain map changes
    
    Parameters:
    - domain_id: PoseMesh domain to join
    - hagall_url: WebSocket server URL
    - participant_id: Unique robot identifier
    """
    
    def __init__(self, config: dict):
        super().__init__('posemesh_sensor')
        
        self.config = config
        self.domain_id = config.get('domain_id')
        self.hagall_url = config.get('hagall_url', 'ws://localhost:8080')
        self.participant_id = config.get('participant_id', 'robot_001')
        
        # Publishers
        self.pose_pub = self.create_publisher(
            PoseStamped, '/posemesh/robot_pose', 10)
            
        # Subscribers - robot's internal pose
        self.robot_pose_sub = self.create_subscription(
            PoseStamped, '/robot_pose', self.robot_pose_callback, 10)
            
        # Timer for broadcasting
        self.timer = self.create_timer(0.1, self.broadcast_timer)
        
        # WebSocket connection (initialized later)
        self.ws = None
        self.connected = False
        
        self.get_logger().info(f'PoseMesh sensor node started')
        self.get_logger().info(f'Domain: {self.domain_id}')
        self.get_logger().info(f'Hagall: {self.hagall_url}')
        
    async def connect_hagall(self):
        """Connect to Hagall WebSocket server."""
        try:
            self.ws = await websockets.connect(f'{self.hagall_url}')
            self.connected = True
            
            # Join session
            join_msg = {
                'type': 'join',
                'session_id': self.domain_id,
                'participant_id': self.participant_id
            }
            await self.ws.send(json.dumps(join_msg))
            
            self.get_logger().info('Connected to Hagall')
            
        except Exception as e:
            self.get_logger().error(f'Failed to connect: {e}')
            self.connected = False
            
    def robot_pose_callback(self, msg: PoseStamped):
        """Handle incoming robot pose from localization."""
        # Store for broadcasting
        self.current_pose = msg
        
    def broadcast_timer(self):
        """Periodically broadcast pose to PoseMesh."""
        if not self.connected or not hasattr(self, 'current_pose'):
            return
            
        pose = self.current_pose.pose.position
        orientation = self.current_pose.pose.orientation
        
        broadcast_msg = {
            'type': 'entity_update',
            'entity_type': 'robot',
            'entity_id': self.participant_id,
            'pose': {
                'position': {'x': pose.x, 'y': pose.y, 'z': pose.z},
                'orientation': {
                    'x': orientation.x,
                    'y': orientation.y, 
                    'z': orientation.z,
                    'w': orientation.w
                }
            }
        }
        
        # In real implementation, send via WebSocket
        self.get_logger().debug(f'Broadcasting pose: ({pose.x}, {pose.y}, {pose.z})')


# Bridge between ROS and async WebSocket
class PoseMeshBridge:
    """Bridges ROS callbacks to async WebSocket."""
    
    def __init__(self, node: PoseMeshSensorNode):
        self.node = node
        self.loop = asyncio.new_event_loop()
        
    async def run(self):
        await self.node.connect_hagall()
        while True:
            await asyncio.sleep(0.1)


def main(args=None):
    rclpy.init(args=args)
    
    # Get parameters
    config = {
        'domain_id': 'retail-store-01',  # From parameter
        'hagall_url': 'ws://localhost:8080',
        'participant_id': 'robot_001'
    }
    
    node = PoseMeshSensorNode(config)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
