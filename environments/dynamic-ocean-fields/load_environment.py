# environments/dynamic-ocean-fields/load_environment.py
"""
Verifiers-compatible loader for Dynamic Ocean Fields.

This module exposes load_environment(...) which the Prime Hub/Verifiers
can import to construct environment instances for evaluation.
"""

from typing import Any, Dict
import json
import os

# Import your local package (must be importable after editable install)
from dynamic_ocean.envs.dynamic_ocean_env import DynamicOceanEnv
from dynamic_ocean.utils.data_loader import load_grid
from dynamic_ocean.envs.cost_functions import aggregate_cost

def load_environment(**kwargs) -> Any:
    """
    Return a factory that creates DynamicOceanEnv instances for rollouts.
    Expected kwargs:
      - grid_path: path to a .npz map (default: data/sample_grid.npz)
      - weights: list of floats (optional)
      - patch_size: int optional
      - max_steps: int optional
    This loader returns a callable (factory) that takes no args and returns a new env.
    The verifiers template may require returning a vf.Environment; adapt if needed.
    """
    # Default to repo root data folder
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    default_grid = os.path.join(repo_root, "dynamic_ocean", "data", "sample_grid.npz")
    grid_path = kwargs.get("grid_path", default_grid)
    # load channels + meta
    channels, meta = load_grid(grid_path)
    weights = kwargs.get("weights", None) or [1.0] * channels.shape[0]
    smooth_sigma = kwargs.get("smooth_sigma", 1.0)
    cost_map = aggregate_cost(channels, weights, smooth_sigma=smooth_sigma)
    start = meta.get("start", (0, 0))
    goal = meta.get("goal", (channels.shape[1] - 1, channels.shape[2] - 1))

    def env_factory():
        return DynamicOceanEnv(cost_map=cost_map, start=start, goal=goal,
                               patch_size=kwargs.get("patch_size", 3),
                               max_steps=kwargs.get("max_steps", None))

    return env_factory
