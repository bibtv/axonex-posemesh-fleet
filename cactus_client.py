"""
Cactus Search Client - Product search and position lookup via Auki Cactus API
"""

import aiohttp
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class CactusClient:
    """Client for Cactus product search API."""
    
    def __init__(self, config: dict):
        self.config = config
        self.api_url = config.get('api_url', 'https://cactus-public-api.lookingglassprotocol.com')
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
            
    async def search_product(self, query: str, limit: int = 10) -> Optional[Dict]:
        """
        Search for a product and get its pose.
        
        Args:
            query: Product name search query
            limit: Maximum results
            
        Returns:
            Product data with pose or None
        """
        endpoint = f"{self.api_url}/search/page"
        
        payload = {
            "query": query,
            "page": 1,
            "page_size": limit
        }
        
        try:
            async with self.session.post(endpoint, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    results = data.get('results', [])
                    if results:
                        # Return first match with pose
                        for product in results:
                            if 'pose' in product:
                                return product
                        # Return first result even without pose
                        return results[0]
                else:
                    logger.error(f"Cactus search failed: {resp.status}")
        except Exception as e:
            logger.error(f"Cactus search error: {e}")
            
        return None
        
    async def get_recommendations(self, product_id: str, limit: int = 5) -> List[Dict]:
        """
        Get product recommendations.
        
        Args:
            product_id: Base product ID
            limit: Number of recommendations
            
        Returns:
            List of recommended products
        """
        endpoint = f"{self.api_url}/recommended"
        
        payload = {
            "product_id": product_id,
            "limit": limit
        }
        
        try:
            async with self.session.post(endpoint, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('results', [])
        except Exception as e:
            logger.error(f"Cactus recommendations error: {e}")
            
        return []


# Example: Using the auki_robotics_cactus_search library directly
# from auki_robotics_cactus_search import CactusAPIClient
#
# client = CactusAPIClient()
# result = await client.search("coke")
# print(result.pose)  # {x, y, z} in domain coordinates
