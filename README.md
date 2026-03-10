# Axonex Fleet Management POC

Proof-of-concept for integrating multiple robot platforms with Auki PoseMesh for shared mapping and fleet coordination in retail environments.

**Supported Robots:**
- **Axonex M series** — Robots with Yunji chassis
- **Rice Robotics** — R1, R2, and other Rice Robotics platforms

## Two Architecture Options

This POC supports **two integration approaches** depending on your needs:

---

## Option A: Centralized (REST API) — Recommended for Quick POC

**Axonex Zero Basic Platform runs on server, communicates with robots via REST API**

```
┌─────────────────────────────────────────────────────────────┐
│              Axonex Zero Basic Platform                     │
│                  (server/cloud)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Cactus     │  │   PoseMesh   │  │    Hagall    │       │
│  │   Search     │  │    Domain    │  │   (Relay)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Axonex M   │    │  Axonex M   │    │    Rice      │
│   series    │    │   series    │    │  Robotics    │
│ (Yunji      │    │ (Yunji      │    │    (R1/R2)   │
│  chassis)   │    │  chassis)   │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

**Files:**
- `fleet_controller.py` — Main orchestration
- `posemesh_connector.py` — PoseMesh API client
- `cactus_client.py` — Product search
- `yunji_client.py` — REST API wrapper

**Pros:** Simple, quick to deploy, works with Yunji's existing API

---

## Option B: Distributed (ROS2) — Recommended for Full Integration

**ROS nodes run on each robot, deeper control + sensor fusion**

```
┌─────────────────────────────────────────────────────────────┐
│              Axonex Zero Basic Platform                     │
│                  (server/cloud)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Cactus     │  │   PoseMesh   │  │    Hagall    │       │
│  │   Search     │  │    Domain    │  │   (Relay)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────┬────────────────────────────────┘
                             │ WebSocket / ROS2 bridge
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               ROBOT 1 (Axonex M series - ROS2)            │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │ yunji_ros_node │◄───│posemesh_sensor │                  │
│  │                 │    │    _node       │                  │
│  └────────┬────────┘    └────────┬────────┘                 │
│           │                      │                           │
│           ▼                      ▼                          │
│    ┌─────────────┐         ┌─────────────┐                  │
│    │   Yunji    │         │  PoseMesh   │                  │
│    │  Chassis   │         │   Network   │                  │
│    └─────────────┘         └─────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

**Files in `ros2/`:**
- `yunji_ros_node.py` — ROS2 driver for Yunji
- `posemesh_sensor_node.py` — PoseMesh integration
- `launch/yunji_posemesh.launch.py` — Launch file
- `package.xml`, `setup.py` — ROS2 package

**Pros:** Full control, sensor fusion, works with ROS ecosystem

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

hagall:
  server: "ws://your-hagall-server:8080"
  session: "retail-store-01"
```

---

## API Keys Required

1. **Auki Console** - https://console.auki.network
2. **Cactus API** - Built into auki_robotics_cactus_search
3. **Yunji API** - Contact Yunji (400-608-0917)
4. **Rice Robotics API** - Contact Rice Robotics

---

## Next Steps

1. [ ] Get Auki Console credentials
2. [ ] Set up PoseMesh domain for test store
3. [ ] Obtain Yunji API access/documentation
4. [ ] Deploy hagall server
5. [ ] Test with single robot
6. [ ] Expand to multi-robot fleet

---

## References

- [auki_robotics_map_utils](https://github.com/aukilabs/auki_robotics_map_utils)
- [auki_robotics_cactus_search](https://github.com/aukilabs/auki_robotics_cactus_search)
- [auki_robotics_domain_calibrator](https://github.com/aukilabs/auki_robotics_domain_calibrator)
- [hagall](https://github.com/aukilabs/hagall)
- [pathfinding](https://github.com/aukilabs/pathfinding)
- [Yunji UP](https://www.yunji.ai/product_up.html)
