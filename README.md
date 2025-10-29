# Dynamic Ocean Fields

A Gymnasium-compatible reinforcement learning environment for ship navigation in dynamic ocean conditions.

## Description

Navigate a ship from start to destination while minimizing cost based on environmental parameters: wave height, current velocity, temperature, and water depth.

## Observation Space

- **Type**: Box(38,)
- **Components**:
  - 3×3 local grid (36 values): 4 features × 9 cells around ship
  - Ship coordinates (2 values): normalized position

## Action Space

- **Type**: Discrete(9)
- **Actions**: 8 directions (N, NE, E, SE, S, SW, W, NW) + stay

## Reward

Negative cost of current cell. Lower environmental costs = higher rewards.

## Episode Termination

- Ship reaches destination (success)
- Maximum steps exceeded (truncated)

## Usage

```python
from load_environment import load_environment

# Load with random grid
env = load_environment(grid_size=(20, 20))

# Or load from file
env = load_environment(grid_path="data/sample_grid.npz")

# Run episode
obs, info = env.reset()
for _ in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

## Installation

```bash
pip install -e .
```

## Features

- 4-channel environmental data (waves, currents, temperature, depth)
- Configurable cost function weights
- A* optimal path baseline
- Sample agents (random, greedy)
- Visualization tools
