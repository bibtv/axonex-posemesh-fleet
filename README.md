# Axonex Zero Fleet Management Platform

Unified fleet controller for retail robots powered by Auki PoseMesh spatial computing.

## Overview

Axonex Zero is a fleet management platform that enables autonomous retail robots to understand and navigate physical spaces using PoseMesh — a shared spatial coordinate system. The platform supports multiple robot brands and integrates with enterprise IoT infrastructure.

**Supported Robots:**
- **Axonex M series** — Robots with Yunji chassis
- **Rice Robotics** — R1, R2, and other Rice Robotics platforms

---

## Use Cases

### 1. Product-Location-Aware Navigation

Customers ask the robot for products, and the robot guides them to the exact shelf location.

- Integrates with **Cactus Search** for product lookup
- Uses **PoseMesh** for precise shelf coordinates
- Robot leads customer via optimized pathfinding

```
Customer: "Find X1 Pro Laptop"
    ↓
Cactus Search → Product location
    ↓
PoseMesh → Shelf coordinates + nav path
    ↓
Robot guides customer to product
```

### 2. Dynamic Fleet Rebalancing

AI-powered fleet optimization that automatically positions robots based on real-time demand.

- **PoseMesh** — Robot positions + navigation
- **Power Workplace Optimus IoT** — Occupancy sensing per zone
- Real-time demand calculation + auto-rebalancing

---

## Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Axonex Zero Platform                         │
│                     (Fleet Controller)                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Cactus     │  │   PoseMesh   │  │   Power Workplace   │  │
│  │   Search     │  │    Domain    │  │   Optimus IoT       │  │
│  │             │  │             │  │   (Occupancy)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│         │               │                    │                   │
│         └───────────────┼────────────────────┘                   │
│                         ▼                                        │
│              ┌──────────────────────┐                             │
│              │  Fleet Orchestrator  │                             │
│              │  • Task Assignment   │                             │
│              │  • Rebalancing       │                             │
│              │  • Path Planning     │                             │
│              └──────────┬───────────┘                             │
└─────────────────────────┼────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Axonex M   │  │  Axonex M   │  │    Rice      │
│   series    │  │   series    │  │  Robotics    │
│ (Yunji      │  │ (Yunji      │  │    (R1/R2)   │
│  chassis)   │  │  chassis)   │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Two Integration Options

#### Option A: Centralized (REST API) — Recommended for Quick POC

Axonex Zero runs on server, communicates with robots via REST API.

```
Axonex Zero (server) ←── HTTP/REST ──→ Robots
```

**Files:**
- `fleet_controller.py` — Main orchestration
- `posemesh_connector.py` — PoseMesh API client
- `cactus_client.py` — Product search
- `yunji_client.py` — REST API wrapper

#### Option B: Distributed (ROS2) — Recommended for Full Integration

ROS nodes run on each robot for deeper control + sensor fusion.

```
Axonex Zero (server) ←─ WebSocket/ROS2 ─→ Robots (ROS2 nodes)
```

**Files in `ros2/`:**
- `yunji_ros_node.py` — ROS2 driver for Yunji
- `posemesh_sensor_node.py` — PoseMesh integration
- `launch/yunji_posemesh.launch.py` — Launch file

---

## Quick Start

### Option A: REST Version

```bash
# Install
pip install -r requirements.txt

# Configure
cp config.example.yaml config.yaml

# Run
python main.py --task "Find Coke"
python main.py --status
```

### Option B: ROS2 Version

```bash
# Copy ros2 package to your ROS2 workspace
cp -r ros2 ~/colcon_ws/src/yunji_ros_driver

# Build
cd ~/colcon_ws
colcon build --packages-select yunji_ros_driver

# Run
ros2 launch yunji_ros_driver yunji_posemesh.launch.py
```

---

## Configuration

```yaml
posemesh:
  account: "your@email.com"
  password: "your-password"
  domain_id: "your-domain-id"

cactus:
  api_url: "https://cactus-public-api.lookingglassprotocol.com"

axonex_m:
  # Axonex M series (Yunji chassis)
  api_url: "http://your-axonex-m-robot:8080"
  robot_ids:
    - "robot-001"
    - "robot-002"

rice_robotics:
  # Rice Robotics platforms (R1, R2, etc.)
  api_url: "http://your-rice-robot:8080"
  robot_ids:
    - "rice-001"
    - "rice-002"

optimus_iot:
  # Power Workplace Optimus IoT Platform
  api_url: "http://your-optimus-server:8080"
  occupancy_enabled: true
  zones:
    - entrance
    - aisle_1_3
    - aisle_4_6
    - aisle_7_9
    - checkout

hagall:
  server: "ws://your-hagall-server:8080"
  session: "retail-store-01"
```

---

## Integrations

| Integration | Purpose |
|------------|---------|
| **Auki PoseMesh** | Spatial positioning, nav mesh, shared coordinate system |
| **Cactus Search** | Product database and location lookup |
| **Power Workplace Optimus IoT** | Occupancy sensing, zone metrics, people counting |
| **Hagall** | Real-time relay for multi-robot coordination |

---

## Documentation

- [Detailed Use Cases](./docs/use_cases.md) — Full narrative and system design
- [Presentation](./docs/presentation.md) — Slide deck format

---

## API Keys Required

1. **Auki Console** — https://console.auki.network
2. **Cactus API** — Built into auki_robotics_cactus_search
3. **Yunji API** — Contact Yunji (400-608-0917)
4. **Rice Robotics API** — Contact Rice Robotics
5. **Power Workplace Optimus IoT** — Contact Power Workplace

---

## Next Steps

1. [ ] Get Auki Console credentials
2. [ ] Set up PoseMesh domain for test store
3. [ ] Configure Optimus IoT occupancy sensors
4. [ ] Obtain robot API access (Yunji / Rice Robotics)
5. [ ] Deploy hagall server
6. [ ] Test with single robot
7. [ ] Expand to multi-robot fleet
8. [ ] Enable auto-rebalancing

---

## References

- [Auki PoseMesh](https://github.com/aukilabs/posemesh)
- [auki_robotics_map_utils](https://github.com/aukilabs/auki_robotics_map_utils)
- [auki_robotics_cactus_search](https://github.com/aukilabs/auki_robotics_cactus_search)
- [domain-viewer](https://github.com/aukilabs/domain-viewer)
- [reconstruction-server](https://github.com/aukilabs/reconstruction-server)
- [hagall](https://github.com/aukilabs/hagall)
- [pathfinding](https://github.com/aukilabs/pathfinding)
- [Yunji UP](https://www.yunji.ai/product_up.html)
