"""
Yunji Robot Client - REST API wrapper for Yunji UP robots

Note: This is a template based on typical robot APIs.
Actual endpoints need to be verified with Yunji documentation.
"""

import aiohttp
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class YunjiClient:
    """Client for Yunji UP robot REST API."""
    
    def __init__(self, config: dict, robot_id: str):
        self.config = config
        self.robot_id = robot_id
        self.base_url = config.get('api_url', 'http://localhost:8080')
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
            
    async def navigate_to(self, x: float, z: float, yaw: float = 0.0) -> str:
        """
        Send navigation command to robot.
        
        Args:
            x: X coordinate in meters
            z: Z coordinate in meters  
            yaw: Rotation in radians
            
        Returns:
            Task ID
        """
        # Yunji API format (template - verify with actual docs)
        endpoint = f"{self.base_url}/api/navigation/move"
        
        payload = {
            "target": {
                "position": {"x": x, "y": 0, "z": z},
                "orientation": {"yaw": yaw}
            },
            "options": {
                "speed": 0.5,  # m/s
                "avoid_obstacles": True
            }
        }
        
        async with self.session.post(endpoint, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get('task_id', '')
            else:
                raise Exception(f"Navigation failed: {resp.status}")
                
    async def stop(self):
        """Emergency stop."""
        endpoint = f"{self.base_url}/api/navigation/stop"
        await self.session.post(endpoint, json={})
        
    async def get_status(self) -> Dict:
        """
        Get robot status.
        
        Returns:
            Status dict with battery, position, state
        """
        endpoint = f"{self.base_url}/api/status"
        
        async with self.session.get(endpoint) as resp:
            if resp.status == 200:
                return await resp.json()
            return {'error': 'Failed to get status'}
            
    async def get_position(self) -> Optional[Dict]:
        """Get current robot position."""
        status = await self.get_status()
        return status.get('position')
        
    async def get_battery(self) -> int:
        """Get battery percentage."""
        status = await self.get_status()
        return status.get('battery', 0)
        
    async def return_to_charging(self):
        """Send robot to charging station."""
        endpoint = f"{self.base_url}/api/navigation/return"
        await self.session.post(endpoint, json={'mode': 'charging'})
        
    async def get_map(self) -> bytes:
        """Get robot's current SLAM map."""
        endpoint = f"{self.base_url}/api/map"
        async with self.session.get(endpoint) as resp:
            if resp.status == 200:
                return await resp.read()
            return b''


# Mock client for testing without real robots
class MockYunjiClient:
    """Mock client for POC testing."""
    
    def __init__(self, config: dict, robot_id: str):
        self.robot_id = robot_id
        self._position = {'x': 0, 'y': 0, 'z': 0}
        self._battery = 85
        self._task_id = 0
        
    async def navigate_to(self, x: float, z: float, yaw: float = 0.0) -> str:
        self._task_id += 1
        self._position = {'x': x, 'y': 0, 'z': z}
        logger.info(f"[MOCK] Robot {self.robot_id} navigating to ({x}, {z})")
        return f"mock-task-{self._task_id}"
        
    async def stop(self):
        logger.info(f"[MOCK] Robot {self.robot_id} stopped")
        
    async def get_status(self) -> Dict:
        return {
            'position': self._position,
            'battery': self._battery,
            'state': 'idle'
        }
        
    async def get_position(self) -> Dict:
        return self._position
        
    async def get_battery(self) -> int:
        return self._battery
        
    async def return_to_charging(self):
        logger.info(f"[MOCK] Robot {self.robot_id} returning to charging")
