"""
Hagall (Relay) Client - Real-time fleet coordination via WebSocket

Hagall is the PoseMesh networking server that handles
real-time position sharing and message broadcasting.
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Callable

logger = logging.getLogger(__name__)


class HagallClient:
    """WebSocket client for Hagall relay server."""
    
    def __init__(self, config: dict):
        self.config = config
        self.server_url = config.get('server', 'ws://localhost:8080')
        self.session_id = config.get('session', 'default')
        self.participant_id: Optional[str] = None
        self.ws: Optional[asyncio.WebSocketServer] = None
        self._callbacks: Dict[str, Callable] = {}
        self._receive_task: Optional[asyncio.Task] = None
        
    async def connect(self, participant_id: Optional[str] = None):
        """
        Connect to Hagall session.
        
        Args:
            participant_id: Optional specific ID, otherwise auto-generated
        """
        self.participant_id = participant_id or f"fleet-controller"
        
        # Note: This is a simplified connection
        # Full implementation would use the hagall protocol
        # See: https://github.com/aukilabs/hagall
        
        logger.info(f"Connected to Hagall session: {self.session_id}")
        logger.info(f"Participant ID: {self.participant_id}")
        
    async def close(self):
        """Disconnect from Hagall."""
        if self._receive_task:
            self._receive_task.cancel()
        logger.info("Disconnected from Hagall")
        
    async def update_robot_pose(self, robot_id: str, pose: dict):
        """
        Broadcast robot position update.
        
        This makes the robot visible to other participants
        in the shared session.
        
        Args:
            robot_id: Robot identifier
            pose: Position {x, y, z, yaw}
        """
        message = {
            "type": "entity_update",
            "entity_type": "robot",
            "entity_id": robot_id,
            "pose": {
                "position": pose,
                "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}
            }
        }
        
        # In real implementation, this would send via WebSocket
        logger.debug(f"Broadcasting pose for {robot_id}: {pose}")
        
    async def send_command(self, robot_id: str, command: dict):
        """
        Send command to specific robot.
        
        Args:
            robot_id: Target robot
            command: Command payload
        """
        message = {
            "type": "command",
            "target": robot_id,
            "payload": command
        }
        
        logger.info(f"Sending command to {robot_id}: {command}")
        
    async def broadcast_message(self, message: dict):
        """Broadcast message to all participants."""
        broadcast_msg = {
            "type": "broadcast",
            "payload": message
        }
        logger.debug(f"Broadcasting: {message}")
        
    def on_participant_joined(self, callback: Callable):
        """Register callback for participant join events."""
        self._callbacks['participant_joined'] = callback
        
    def on_participant_left(self, callback: Callable):
        """Register callback for participant leave events."""
        self._callbacks['participant_left'] = callback
        
    def on_entity_update(self, callback: Callable):
        """Register callback for entity pose updates."""
        self._callbacks['entity_update'] = callback
        
    async def get_participants(self) -> list:
        """Get list of participants in session."""
        # Would query hagall for current participants
        return []
        
    async def get_robot_positions(self) -> Dict[str, dict]:
        """
        Get positions of all robots in fleet.
        
        Returns:
            Dict of robot_id -> position
        """
        positions = {}
        # In real implementation, query from hagall state
        return positions


# Example message format from Hagall protocol:
"""
Hagall uses binary/protobuf messages. JSON equivalent:

Join Session:
{"type": "join", "session_id": "retail-01", "participant_id": "robot-001"}

Entity Update (pose broadcast):
{
  "type": "entity_update",
  "entity_id": "robot-001",
  "pose": {
    "position": {"x": 1.0, "y": 0.0, "z": 2.0},
    "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}
  }
}

Command:
{
  "type": "command",
  "target": "robot-001",
  "command": "navigate",
  "params": {"x": 5.0, "z": 3.0}
}
"""
