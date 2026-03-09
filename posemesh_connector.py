"""
PoseMesh Connector - Handles connection to Auki PoseMesh network
"""

import aiohttp
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class PoseMeshConnector:
    """Connects to PoseMesh domain for shared mapping."""
    
    def __init__(self, config: dict):
        self.config = config
        self.domain_id = config.get('domain_id')
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = "https://dsc.auki.network/spatial"
        
    async def connect(self):
        """Establish connection to PoseMesh."""
        self.session = aiohttp.ClientSession()
        logger.info(f"Connected to PoseMesh domain: {self.domain_id}")
        
    async def close(self):
        """Close connection."""
        if self.session:
            await self.session.close()
            
    async def get_map(self, resolution: int = 20) -> bytes:
        """
        Retrieve the 2D map from the domain.
        
        Args:
            resolution: Pixels per meter (default 20)
            
        Returns:
            Map image bytes
        """
        # This mimics auki_robotics_map_utils retrieve_map.py
        # In production, you'd use the actual library
        endpoint = f"{self.base_url}/crosssection"
        
        payload = {
            "domain_id": self.domain_id,
            "resolution": resolution
        }
        
        async with self.session.post(endpoint, json=payload) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                raise Exception(f"Failed to get map: {resp.status}")
                
    async def get_navigable_position(self, target_pose: dict) -> dict:
        """
        Get the nearest navigable position to a target.
        
        This uses the navmesh optimization from auki_robotics_map_utils
        to find a valid position the robot can actually reach.
        
        Args:
            target_pose: Target position {x, y, z}
            
        Returns:
            Navigable position {x, y, z, yaw}
        """
        endpoint = f"{self.base_url}/restricttonavmesh"
        
        payload = {
            "domain_id": self.domain_id,
            "target": target_pose
        }
        
        async with self.session.post(endpoint, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get('navigable_position', target_pose)
            else:
                # Fallback: return original target
                logger.warning(f"Navmesh query failed, using original target")
                return target_pose
                
    async def raycast(self, origin_pose: dict, direction: dict) -> Optional[dict]:
        """
        Cast a ray to detect intersection with digital objects.
        
        Args:
            origin_pose: Origin transformation matrix
            direction: Ray direction vector
            
        Returns:
            Hit data or None
        """
        endpoint = f"{self.base_url}/raycast"
        
        payload = {
            "domain_id": self.domain_id,
            "origin": origin_pose,
            "direction": direction
        }
        
        async with self.session.post(endpoint, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get('hits', [])
            return None
            
    async def get_route(self, waypoints: list) -> list:
        """
        Optimize route through multiple waypoints.
        
        Args:
            waypoints: List of {x, y, z} positions
            
        Returns:
            Optimized waypoints on navmesh
        """
        endpoint = f"{self.base_url}/pathfind"
        
        payload = {
            "domain_id": self.domain_id,
            "waypoints": waypoints
        }
        
        async with self.session.post(endpoint, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get('onmesh_waypoints', waypoints)
            return waypoints


# Example usage
async def main():
    config = {
        'domain_id': 'your-domain-id',
        'account': 'user@email.com',
        'password': 'pass'
    }
    
    connector = PoseMeshConnector(config)
    await connector.connect()
    
    # Get navigable position near a shelf
    target = {'x': 5.0, 'y': 0.0, 'z': 3.0}  # Shelf position
    navigable = await connector.get_navigable_position(target)
    print(f"Navigable position: {navigable}")
    
    await connector.close()


if __name__ == "__main__":
    asyncio.run(main())
