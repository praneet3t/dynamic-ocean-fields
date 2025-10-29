# Dynamic Ocean Fields

A reinforcement learning environment for ship navigation in dynamic ocean conditions. The environment simulates a 2D ocean grid where each cell contains environmental parameters (wave height, current velocity, temperature, depth) that affect navigation costs.

## Overview

**Goal**: Navigate a ship from start to destination while minimizing total cost based on environmental conditions.

**Environment**: 2D grid where each cell has 4 environmental features combined into a cost function.

**Compatibility**: Built for Gymnasium (OpenAI Gym v1) for easy integration with RL algorithms.

## Installation

```bash
# Create conda environment
conda create -n ocean-env python=3.8
conda activate ocean-env

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from envs.dynamic_ocean_env import DynamicOceanEnv
from utils.data_loader import generate_sample_grid

# Create environment
grid_data = generate_sample_grid(height=20, width=20)
env = DynamicOceanEnv(grid_data=grid_data)

# Run episode
obs, info = env.reset()
for _ in range(100):
    action = env.action_space.sample()  # Random action
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

# data/ folder — sample grids and data notes

This folder holds sample grids used for testing and demo purposes.

Files:
- sample_grid.npy (NOT included by default) — use the data_loader utility to generate or convert your own grid.
- README.md — this file.

Grid format:
- A spatial grid is stored as a numpy `.npz` or `.npy` file.
- We expect channels stored as a single 3D NumPy array with shape `(C, H, W)`.
  - Typical channels: [wave_height, current_magnitude, obstacle_flag, depth_normed, ...]
- Each channel should be real numbers. The hub's cost aggregation pipeline will normalize channels automatically.

To generate a random sample grid run the provided utility:
```bash
python -m utils.data_loader --generate-sample --out data/sample_grid.npz --seed 42


## Environment Details

### Observation Space
- **Local Grid**: 3×3 grid centered on ship position (4 features × 9 cells = 36 values)
- **Coordinates**: Normalized ship position (2 values)
- **Total**: 38-dimensional continuous space

### Action Space
- **9 discrete actions**: 8 directions (N, NE, E, SE, S, SW, W, NW) + stay
- Actions are clipped to grid boundaries

### Reward Function
- **Reward = -cost** of current grid cell
- Lower environmental costs = higher rewards
- Episode ends when ship reaches destination or exceeds step limit

### Cost Function
Environmental features and their contributions to cost:

1. **Wave Height** (weight: 1.0): Higher waves = higher cost
2. **Current Velocity** (weight: 0.8): Stronger currents = higher cost  
3. **Temperature** (weight: 0.3): Deviation from optimal (0.5) = higher cost
4. **Depth** (weight: 0.5): Shallow water = higher cost

## Usage Examples

### Run Demo
```bash
python main.py
```

### Test Agents
```python
from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent

# Create agents
random_agent = RandomAgent(env.action_space)
greedy_agent = GreedyAgent(env.action_space, env.target_pos)

# Run episodes
obs, _ = env.reset()
action = greedy_agent.act(obs)
```

### Visualize Environment
```python
from utils.visualization import plot_grid_heatmap, plot_route

# Plot environmental features
plot_grid_heatmap(grid_data, feature_idx=0, title="Wave Height")

# Plot navigation route
plot_route(grid_data, route, start_pos, target_pos)
```

### Find Optimal Path
```python
from utils.pathfinding import astar_pathfind

optimal_path, cost = astar_pathfind(grid_data, start_pos, target_pos)
print(f"Optimal path: {len(optimal_path)} steps, cost: {cost:.2f}")
```

## Project Structure

```
dynamic-ocean-fields/
├── envs/                   # Core environment
│   ├── dynamic_ocean_env.py    # Main Gymnasium environment
│   └── cost_functions.py       # Cost calculation logic
├── data/                   # Ocean data
│   ├── sample_grid.npy         # Sample 20×20 grid
│   └── README.md               # Data format documentation
├── utils/                  # Utilities
│   ├── data_loader.py          # Data loading/generation
│   ├── visualization.py        # Plotting functions
│   └── pathfinding.py          # A* baseline algorithm
├── agents/                 # Agent implementations
│   ├── random_agent.py         # Random baseline
│   ├── greedy_agent.py         # Greedy cost-minimizing agent
│   └── rl_agent.py             # RL agent placeholder
├── notebooks/              # Jupyter demos
│   └── demo_env.ipynb          # Environment demonstration
├── tests/                  # Unit tests
├── configs/                # Configuration files
└── main.py                 # Entry point
```

## Configuration

Edit `configs/env_config.yaml` to customize:

- Grid dimensions
- Start/target positions  
- Cost function weights
- Episode parameters

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_env.py
```

## Extending the Environment

### Add New Environmental Features
1. Modify `generate_sample_grid()` in `utils/data_loader.py`
2. Update `calculate_cell_cost()` in `envs/cost_functions.py`
3. Adjust observation space in `DynamicOceanEnv`

### Implement RL Agents
Use the `RLAgent` placeholder in `agents/rl_agent.py`:

```python
# Example: DQN integration
from stable_baselines3 import DQN

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

### Real Ocean Data
Replace sample data with real oceanographic data:
- NOAA Ocean Service
- Copernicus Marine Service  
- ECMWF ERA5 reanalysis

Convert to normalized 4-channel format (see `data/README.md`).

## Performance Baselines

| Agent | Success Rate | Avg Steps | Avg Reward |
|-------|-------------|-----------|------------|
| Random | ~10% | 500 | -150 |
| Greedy | ~80% | 25 | -45 |
| A* Optimal | 100% | 20 | -35 |

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request