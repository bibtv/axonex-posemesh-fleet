# Yunji + PoseMesh Fleet Management POC

Proof-of-concept for integrating Yunji robots with Auki PoseMesh for shared mapping and fleet coordination in retail environments.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Task Dispatcher                          │
│   (Natural language: "Get Coke from aisle 3")             │
└─────────────────────────┬─────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │   Cactus    │ │    PoseMesh │ │    Hagall   │
   │   Search    │ │   Domain    │ │   (Relay)   │
   │ Product→Pose│ │  Shared Map │ │ Fleet State │
   └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
              ┌─────────────────────┐
              │   Fleet Controller  │
              │   (Route Planning)  │
              └──────────┬──────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
┌────────────┐    ┌────────────┐    ┌────────────┐
│   Yunji    │    │   Yunji    │    │   Yunji    │
│  Robot #1  │    │  Robot #2  │    │  Robot #3  │
│ +PoseMesh   │    │ +PoseMesh   │    │ +PoseMesh   │
└────────────┘    └────────────┘    └────────────┘
```

## Components

### 1. Fleet Controller (`fleet_controller.py`)
- Manages pool of Yunji robots
- Assigns tasks based on availability and proximity
- Tracks robot states (idle, busy, charging)

### 2. PoseMesh Connector (`posemesh_connector.py`)
- Connects to Auki network
- Handles domain map retrieval
- Provides navmesh routing

### 3. Cactus Search Client (`cactus_client.py`)
- Product search API
- Returns product poses in domain coordinates

### 4. Yunji API Wrapper (`yunji_client.py`)
- REST API wrapper for Yunji robot commands
- Start/stop navigation
- Status queries

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp config.example.yaml config.yaml
# Edit config.yaml with your credentials

# Run POC
python main.py --task "Find Coke in aisle 3"
```

## Configuration

Edit `config.yaml`:

```yaml
posemesh:
  account: "your@email.com"
  password: "your-password"
  domain_id: "your-domain-id"

cactus:
  api_url: "https://cactus-public-api.lookingglassprotocol.com"

yunji:
  api_url: "http://your-yunji-robot:8080"
  robot_ids:
    - "robot-001"
    - "robot-002"

hagall:
  server: "ws://your-hagall-server:8080"
  session: "retail-store-01"
```

## API Keys Required

1. **Auki Console** - https://console.auki.network
2. **Cactus API** - Built into auki_robotics_cactus_search
3. **Yunji API** - From Yunji documentation

## Next Steps

1. [ ] Get Auki Console credentials
2. [ ] Set up PoseMesh domain for test store
3. [ ] Obtain Yunji robot API access
4. [ ] Deploy hagall server (self-hosted or cloud)
5. [ ] Test single robot integration
6. [ ] Expand to multi-robot fleet

## References

- [auki_robotics_map_utils](https://github.com/aukilabs/auki_robotics_map_utils)
- [auki_robotics_cactus_search](https://github.com/aukilabs/auki_robotics_cactus_search)
- [auki_robotics_domain_calibrator](https://github.com/aukilabs/auki_robotics_domain_calibrator)
- [hagall](https://github.com/aukilabs/hagall)
- [pathfinding](https://github.com/aukilabs/pathfinding)
- [Yunji UP](https://www.yunji.ai/product_up.html)
