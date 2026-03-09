"""
Fleet Controller - Manages pool of Yunji robots and task assignment
"""

import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RobotState(Enum):
    IDLE = "idle"
    BUSY = "busy"
    CHARGING = "charging"
    OFFLINE = "offline"


@dataclass
class Robot:
    id: str
    state: RobotState = RobotState.IDLE
    current_task: Optional[str] = None
    position: Optional[dict] = None  # {x, y, z}
    battery: int = 100


class FleetController:
    """Manages fleet of Yunji robots and assigns tasks."""
    
    def __init__(self, config: dict):
        self.config = config
        self.robots: dict[str, Robot] = {}
        self.posemesh = None
        self.cactus = None
        self.hagall = None
        
    async def initialize(self):
        """Initialize all connections."""
        from posemesh_connector import PoseMeshConnector
        from cactus_client import CactusClient
        from hagall_client import HagallClient
        
        self.posemesh = PoseMeshConnector(self.config['posemesh'])
        await self.posemesh.connect()
        
        self.cactus = CactusClient(self.config['cactus'])
        
        self.hagall = HagallClient(self.config['hagall'])
        await self.hagall.connect()
        
        # Initialize robot pool
        for robot_id in self.config['yunji']['robot_ids']:
            self.robots[robot_id] = Robot(id=robot_id)
            
        logger.info(f"Fleet initialized with {len(self.robots)} robots")
        
    async def assign_task(self, product_name: str, location: str) -> str:
        """
        Assign a task to the best available robot.
        
        Args:
            product_name: Product to retrieve (e.g., "Coke")
            location: Location hint (e.g., "aisle 3")
            
        Returns:
            Task ID
        """
       1. Search #  for product position via Cactus
        product_pose = await self.cactus.search_product(product_name)
        if not product_pose:
            raise ValueError(f"Product '{product_name}' not found")
            
        # 2. Get navmesh-optimized target position
        target_pose = await self.posemesh.get_navigable_position(product_pose)
        
        # 3. Find best robot (idle, closest)
        robot = self._select_best_robot(target_pose)
        if not robot:
            raise RuntimeError("No available robots")
            
        # 4. Assign task
        robot.state = RobotState.BUSY
        robot.current_task = f"Get {product_name}"
        
        # 5. Send command to Yunji robot
        from yunji_client import YunjiClient
        yunji = YunjiClient(self.config['yunji'], robot.id)
        task_id = await yunji.navigate_to(target_pose['x'], target_pose['z'])
        
        # 6. Register with hagall for tracking
        await self.hagall.update_robot_pose(robot.id, target_pose)
        
        logger.info(f"Task assigned: {robot.id} -> {product_name} at {target_pose}")
        return task_id
        
    def _select_best_robot(self, target_pose: dict) -> Optional[Robot]:
        """Select the best robot for a task."""
        available = [r for r in self.robots.values() if r.state == RobotState.IDLE]
        if not available:
            return None
            
        # Simple selection: first available
        # TODO: Add proximity calculation using hagall positions
        return available[0]
        
    async def get_fleet_status(self) -> dict:
        """Get status of all robots in fleet."""
        status = {}
        for robot_id, robot in self.robots.items():
            # Update from actual robot status
            try:
                from yunji_client import YunjiClient
                yunji = YunjiClient(self.config['yunji'], robot_id)
                robot_info = await yunji.get_status()
                status[robot_id] = {
                    'state': robot.state.value,
                    'battery': robot_info.get('battery', robot.battery),
                    'position': robot_info.get('position', robot.position),
                    'task': robot.current_task
                }
            except Exception as e:
                logger.warning(f"Failed to get status for {robot_id}: {e}")
                status[robot_id] = {
                    'state': robot.state.value,
                    'error': str(e)
                }
        return status
