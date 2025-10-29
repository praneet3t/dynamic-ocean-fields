# Dynamic Ocean Fields

A Gymnasium-compatible reinforcement learning environment for ship navigation in dynamic ocean conditions.

## Description

Navigate a ship from start to destination while minimizing cost based on environmental parameters: wave height, current velocity, temperature, and water depth.

## Observation Space

- **Type**: Dict with keys:
  - `local_patch`: Box(1, 3, 3) - 3×3 local cost grid around agent
  - `agent_pos`: Box(2,) - current position (row, col)
  - `goal_pos`: Box(2,) - goal position (row, col)

## Action Space

- **Type**: Discrete(9)
- **Actions**: 0=stay, 1=N, 2=NE, 3=E, 4=SE, 5=S, 6=SW, 7=W, 8=NW

## Reward

Negative cost of current cell. Lower environmental costs = higher rewards.

## Episode Termination

- Ship reaches destination (success)
- Maximum steps exceeded (truncated)

## Usage

```python
from load_environment import load_environment

# Load environment factory
env_factory = load_environment(grid_path="data/sample_grid.npz")
env = env_factory()

# Run episode
obs, info = env.reset()
for _ in range(100):
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    if done:
        break
```
