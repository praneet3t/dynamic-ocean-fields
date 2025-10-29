"""Load function for Dynamic Ocean Fields environment."""

from dynamic_ocean.envs import DynamicOceanEnv
from dynamic_ocean.utils.data_loader import generate_random_grid, load_grid
from dynamic_ocean.envs.cost_functions import aggregate_cost
import numpy as np


def load_environment(grid_path=None, **kwargs):
    """
    Load the Dynamic Ocean Fields environment.
    
    Args:
        grid_path: Path to .npz grid file. If None, generates random grid.
        **kwargs: Additional arguments:
            - start: tuple (row, col), default (0, 0)
            - goal: tuple (row, col), default (H-1, W-1)
            - patch_size: int, default 3
            - max_steps: int, optional
            - grid_size: tuple (height, width) if generating random grid, default (20, 20)
    
    Returns:
        DynamicOceanEnv: Configured environment instance
    """
    if grid_path:
        channels, meta = load_grid(grid_path)
    else:
        grid_size = kwargs.pop('grid_size', (20, 20))
        channels = generate_random_grid(C=4, H=grid_size[0], W=grid_size[1], seed=42)
    
    # Aggregate channels into single cost map (H, W)
    # Default weights: [wave_height, current_vel, temp, depth]
    weights = kwargs.pop('cost_weights', [1.0, 0.8, 0.3, 0.5])
    cost_map = aggregate_cost(channels, weights=weights)
    H, W = cost_map.shape
    
    # Set defaults
    start = kwargs.pop('start', (0, 0))
    goal = kwargs.pop('goal', (H-1, W-1))
    
    env = DynamicOceanEnv(cost_map=cost_map, start=start, goal=goal, **kwargs)
    return env
