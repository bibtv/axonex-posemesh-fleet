"""
Main entry point for Yunji + PoseMesh Fleet POC
"""

import asyncio
import argparse
import logging
import yaml
from fleet_controller import FleetController

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser(description='Yunji PoseMesh Fleet POC')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--task', help='Task to execute (e.g., "Find Coke")')
    parser.add_argument('--status', action='store_true', help='Show fleet status')
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize fleet controller
    fleet = FleetController(config)
    await fleet.initialize()
    
    try:
        if args.task:
            # Execute task
            logger.info(f"Executing task: {args.task}")
            task_id = await fleet.assign_task(
                product_name=args.task,
                location=""
            )
            logger.info(f"Task assigned: {task_id}")
            
        elif args.status:
            # Show fleet status
            status = await fleet.get_fleet_status()
            print("\n=== Fleet Status ===")
            for robot_id, info in status.items():
                print(f"\n{robot_id}:")
                print(f"  State: {info.get('state', 'unknown')}")
                print(f"  Battery: {info.get('battery', 'N/A')}%")
                print(f"  Position: {info.get('position', 'N/A')}")
                print(f"  Task: {info.get('task', 'None')}")
        else:
            print("Use --task 'product name' or --status")
            
    finally:
        await fleet.posemesh.close()
        if fleet.hagall:
            await fleet.hagall.close()


if __name__ == "__main__":
    asyncio.run(main())
