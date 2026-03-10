# Axonex Zero + PoseMesh Use Cases

## Detailed Narrative & Design

---

# Use Case 1: Product-Location-Aware Navigation

## Narrative

### The Scenario

It's Saturday afternoon at a large electronics retailer. A customer walks in looking for a specific laptop — the "X1 Pro 15-inch" in the tech section. Without PoseMesh, they'd:
- Wander aisles looking for signage
- Ask a staff member who may be busy
- Give up and leave frustrated

### With Axonex Zero + PoseMesh

**Step 1: Customer Request**
The customer approaches a robot or uses a kiosk/integrated app:

> *"Find X1 Pro 15-inch laptop"*

**Step 2: AI Processing**
- Cactus Search API identifies the product → returns location data
- Axonex Zero receives product coordinates from PoseMesh domain

**Step 3: Guided Navigation**
The robot responds:

> "I found it! It's in Aisle 7, Section C — about 40 meters away. Would you like me to guide you there?"

**Step 4: Robot Leads**
- Robot turns on navigation display
- Walks ahead at comfortable pace
- Customer follows the robot's screen/path

**Step 5: Arrival**
> "Here's the X1 Pro 15-inch. It's on the middle shelf, third from the left. Need help with anything else?"

---

### Benefits

| Stakeholder | Benefit |
|-------------|---------|
| **Customer** | Frictionless shopping, no asking around |
| **Staff** | Less interrupted, focus on sales |
| **Store** | Higher conversion, faster customer throughput |

---

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                      Axonex Zero Platform                       │
│                    (Fleet Controller / Cloud)                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Cactus     │  │   PoseMesh   │  │    Hagall           │  │
│  │   Search     │  │    Domain    │  │   (Real-time)       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│         ▼                 ▼                      ▼               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Navigation Engine                               │ │
│  │  • Product location → coordinates                           │ │
│  │  • Pathfinding through navmesh                              │ │
│  │  • Real-time robot position updates                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │         Robot (Axonex M)     │
              │  ┌─────────────────────────┐│
              │  │    Navigation Display   ││
              │  │    (GUI / Screen)       ││
              │  └─────────────────────────┘│
              │                             │
              │  ┌─────────────────────────┐│
              │  │    PoseMesh Client      ││
              │  │    (Position + Map)     ││
              │  └─────────────────────────┘│
              └─────────────────────────────┘
```

### Data Flow

```
User Query: "Find X1 Pro"
       │
       ▼
┌──────────────┐     ┌─────────────┐
│   Cactus     │────►│   Product   │
│   Search     │     │   Location  │
└──────────────┘     └──────┬──────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   PoseMesh Domain   │
                 │  (Get coords +      │
                 │   navmesh path)     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Axonex Zero       │
                 │   Fleet Controller  │
                 └──────────┬──────────┘
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Robot A    │      │  Robot B    │      │   Mobile    │
│  (Navigate) │      │  (Standby)  │      │   App       │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## Example UI

### Screen 1: Initial Request

```
┌─────────────────────────────────────────┐
│  🛒 Smart Retail Assistant               │
├─────────────────────────────────────────┤
│                                         │
│      🤖                                 │
│                                         │
│   "What are you looking for?"           │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │ 🔍 Search products...           │   │
│   └─────────────────────────────────┘   │
│                                         │
│   Suggestions:                          │
│   📱 Phones   💻 Laptops   🎧 Audio    │
│                                         │
├─────────────────────────────────────────┤
│  🗺️ Map  │  🚶 Follow Me  │  ℹ️ Help   │
└─────────────────────────────────────────┘
```

### Screen 2: Product Found

```
┌─────────────────────────────────────────┐
│  ✅ Product Found!                      │
├─────────────────────────────────────────┤
│                                         │
│   🖥️ X1 Pro 15-inch Laptop             │
│                                         │
│   📍 Aisle 7, Section C                │
│   📏 ~40 meters away                   │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │     [ 🚶 Follow Me ]            │   │
│   └─────────────────────────────────┘   │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │     [ 📍 Show on Map ]          │   │
│   └─────────────────────────────────┘   │
│                                         │
├─────────────────────────────────────────┤
│  🔙 Back                                │
└─────────────────────────────────────────┘
```

### Screen 3: Navigation Active

```
┌─────────────────────────────────────────┐
│  🚶 Guiding to: X1 Pro                  │
├─────────────────────────────────────────┤
│                                         │
│      ┌─────────────────────────┐        │
│      │                         │        │
│      │    🗺️  NAVIGATION      │        │
│      │                         │        │
│      │   You ◄── Robot        │        │
│      │    │                   │        │
│      │    ▼                   │        │
│      │   [📍]                │        │
│      │                         │        │
│      └─────────────────────────┘        │
│                                         │
│   📍 Destination: Aisle 7, Sec C      │
│   ⏱️ ETA: 2 minutes                    │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │     [ ⏹️ Stop Navigation ]     │   │
│   └─────────────────────────────────┘   │
│                                         │
├─────────────────────────────────────────┤
│  🤖 Robot #3 • Following                │
└─────────────────────────────────────────┘
```

### Screen 4: Arrival

```
┌─────────────────────────────────────────┐
│  🎉 You're Here!                        │
├─────────────────────────────────────────┤
│                                         │
│   🖥️ X1 Pro 15-inch Laptop             │
│                                         │
│   ┌───────────────────────────────┐    │
│   │                               │    │
│   │     🖥️💻🖱️                  │    │
│   │                               │    │
│   │   Middle shelf, 3rd from left │    │
│   │                               │    │
│   └───────────────────────────────┘    │
│                                         │
│   💰 $1,499.00                          │
│   📦 In stock                           │
│                                         │
│   ┌──────────────┐  ┌──────────────┐    │
│   │ 📞 Call     │  │ 🛒 Add to   │    │
│   │   Staff     │  │   Cart      │    │
│   └──────────────┘  └──────────────┘    │
│                                         │
├─────────────────────────────────────────┤
│  🔙 New Search                          │
└─────────────────────────────────────────┘
```

---

---

# Use Case 4: Dynamic Fleet Rebalancing

## Narrative

### The Scenario

It's 2 PM on a weekday — a quiet time. The store has 3 robots deployed:
- Robot A: Near entrance (idle)
- Robot B: Aisle 5 (stock check)
- Robot C: Checkout area (queue monitoring)

Then, a rush hits. Within 15 minutes:
- 20 customers enter
- 8 need product help
- 5 need checkout assistance

### Without PoseMesh
- Staff scramble to direct robots
- Customers wait
- Robots work suboptimally

### With Axonex Zero + PoseMesh

**2:05 PM — Rush Detected**

```
System Alert: Customer inflow +340% (normal: 6/min → 20/min)
```

**Step 1: Real-Time Assessment**
Axonex Zero polls PoseMesh domain:

> "Where is everyone?"

```
Robot A: Entrance │ (idle) │ Battery 85%
Robot B: Aisle 5 │ (stock) │ Battery 60%
Robot C: Checkout│ (queue) │ Battery 92%
```

> "Where are customers?"

```
Entrance: 12 waiting
Product queries: 8
Checkout queue: 5
```

**Step 2: Intelligent Rebalancing**

Axonex Zero calculates optimal positions:

> "Robot B — abandon stock check, proceed to Aisle 7 (high demand)"
> "Robot A — move to entrance, handle greeting + navigation"
> "Robot C — maintain checkout position"

**Step 3: Autonomous Movement**

```
Robot A → Entrance (greeting duty)
    ┌──────────────────────────┐
    │ "Welcome! Need help      │
    │  finding anything?"     │
    └──────────────────────────┘

Robot B → Aisle 7 (product help)
    ┌──────────────────────────┐
    │ "I can show you to       │
    │  the popular items!"     │
    └──────────────────────────┘

Robot C → Checkout (maintain)
    ┌──────────────────────────┐
    │ "Queue: 5 customers      │
    │  Est. wait: 3 min"       │
    └──────────────────────────┘
```

**Step 4: Continuous Optimization**

As customer flow changes:
- Robots dynamically reposition
- Idle robots auto-relocate to high-traffic zones
- When queue clears → Robot C returns to patrol

---

### Benefits

| Aspect | Improvement |
|--------|-------------|
| **Response time** | Instant rebalancing vs. manual dispatch |
| **Customer satisfaction** | No waiting for assistance |
| **Robot utilization** | 40% higher (idle time reduced) |
| **Staff workload** | 30% fewer interruptions |

---

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Axonex Zero Platform                         │
│                   (Fleet Intelligence)                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Fleet Orchestrator                           │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐   │  │
│  │  │  Demand     │  │  Position   │  │    Task        │   │  │
│  │  │  Predictor │  │  Tracker    │  │    Manager     │   │  │
│  │  └─────────────┘  └──────────────┘  └────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Rebalancing Engine                          │  │
│  │  • Evaluate current positions                            │  │
│  │  • Calculate optimal distribution                        │  │
│  │  • Generate movement commands                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Robot A       │  │   Robot B       │  │   Robot C       │
│                 │  │                 │  │                 │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │ PoseMesh    │ │  │ │ PoseMesh    │ │  │ │ PoseMesh    │ │
│ │ Client      │ │  │ │ Client      │ │  │ │ Client      │ │
│ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │    PoseMesh Domain   │
                   │  (Shared Map +       │
                   │   Positions)         │
                   └─────────────────────┘
```

### Rebalancing Algorithm

```
1. INPUT: Current state
   - Robot positions (x, y)
   - Robot status (idle/busy/charging)
   - Customer positions (heatmap)
   - Task queue

2. CALCULATE: Demand scores per zone
   demand[zone] = customers[zone] + pending_tasks[zone]

3. OPTIMIZE: Minimize total travel + maximize coverage
   For each robot:
     - Find zone with highest demand within range
     - Consider battery constraints
     - Avoid robot-robot collisions

4. EXECUTE: Send movement commands
   - Move to optimal zone
   - Update status

5. LOOP: Every 30 seconds
   - Re-evaluate
   - Adjust if needed
```

---

## Example UI

### Dashboard: Fleet Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 Axonex Zero Fleet Control                    📊 Dashboard  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    STORE MAP                            │   │
│   │                                                          │   │
│   │     ┌────┐          ┌────┐          ┌────┐             │   │
│   │     │Aisle│         │Aisle│         │Aisle│            │   │
│   │     │ 1-3 │         │ 4-6 │         │ 7-9 │            │   │
│   │     └────┘          └────┘          └────┘            │   │
│   │                                                          │   │
│   │    🤖A ●──────────────────────────────● 🤖B            │   │
│   │       │                              │                 │   │
│   │       │        📍 Customer          │                 │   │
│   │       │           Heatmap            │                 │   │
│   │       │                              │                 │   │
│   │    ┌──┴──┐                     ┌─────┴────┐            │   │
│   │    │Entr│                     │ Checkout │            │   │
│   │    └──┬──┘                     └─────┬────┘            │   │
│   │       │                              │ 🤖C             │   │
│   │       └──────────────────────────────┘                 │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│   │ 🤖 Robot A │  │ 🤖 Robot B │  │ 🤖 Robot C │               │
│   │ Entrance   │  │ Aisle 7    │  │ Checkout   │               │
│   │ 🟢 Active │  │ 🟡 Moving  │  │ 🟢 Active  │               │
│   │ 🔋 85%   │  │ 🔋 60%    │  │ 🔋 92%    │               │
│   └────────────┘  └────────────┘  └────────────┘               │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  📈 Stats: Active 3 │ Idle 0 │ Tasks Today: 47 │ 👍 94%       │
└─────────────────────────────────────────────────────────────────┘
```

### Alert: Rebalancing Notification

```
┌─────────────────────────────────────────┐
│  ⚡ Fleet Rebalancing                   │
├─────────────────────────────────────────┤
│                                         │
│   Optimizing robot positions...        │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │  🤖 Robot B: Aisle 7 → Aisle 3  │   │
│   │     Reason: High demand zone    │   │
│   │     ETA: 45 seconds             │   │
│   └─────────────────────────────────┘   │
│                                         │
│   Current demand:                       │
│   📍 Entrance: 12 customers             │
│   📍 Products: 8 queries               │
│   📍 Checkout: 5 in queue             │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │        [ Cancel ]               │   │
│   └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### Settings: Rebalancing Configuration

```
┌─────────────────────────────────────────┐
│  ⚙️ Fleet Settings                      │
├─────────────────────────────────────────┤
│                                         │
│   Auto-Rebalancing         [ ON  ]     │
│                                         │
│   Sensitivity                          │
│   ○ Conservative                       │
│   ● Adaptive (recommended)             │
│   ○ Aggressive                         │
│                                         │
│   Rebalance Interval                   │
│   [ 30 seconds ]                        │
│                                         │
│   Minimum Battery %                    │
│   [ 20% ] ← Return to charging        │
│                                         │
│   ─────────────────────────────────    │
│                                         │
│   Zone Settings                        │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │ High Priority Zones              │   │
│   │ • Entrance                       │   │
│   │ • Checkout                       │   │
│   │ • Customer Service               │   │
│   └─────────────────────────────────┘   │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │ Low Priority Zones               │   │
│   │ • Back storage                   │   │
│   │ • Staff areas                    │   │
│   └─────────────────────────────────┘   │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │      [ Save Settings ]         │   │
│   └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Summary

| Feature | Use Case 1 | Use Case 4 |
|---------|------------|------------|
| **Primary User** | Customer | Store Operator |
| **Core Value** | Navigation | Fleet Optimization |
| **PoseMesh Role** | Product coordinates + navmesh | Real-time positions |
| **Key Integration** | Cactus Search | Hagall / Fleet Controller |
| **POC Complexity** | Medium | Medium-High |

Both use cases demonstrate PoseMesh's core strengths: **spatial awareness** and **shared coordinate system** — enabling robots to understand and navigate the same space as customers and each other.
