# environments/dynamic-ocean-fields/load_environment.py
"""
Stub loader for Prime/verifiers.
This file must provide load_environment(**kwargs) which the Hub will call.
Keep the logic light: parse kwargs, create dataset or cost map, return an Environment object.
"""

from typing import Any
# import verifiers if you plan to use their Environment classes
# import verifiers as vf

# import your env constructor
from dynamic_ocean.envs.dynamic_ocean_env import DynamicOceanEnv
from dynamic_ocean.utils.data_loader import load_grid
from dynamic_ocean.envs.cost_functions import aggregate_cost

def load_environment(*, grid_path: str = "data/sample_grid.npz", weights=None, **kwargs) -> Any:
    """
    Must be importable by the Hub. It should return a verifiers-compatible Environment
    or an object the Hub can use. The exact type depends on the verifiers API in use.
    For now, return a factory function or a simple object wrapping your DynamicOceanEnv.
    The Hub's stub will guide you; adapt to the verifiers template if it requires vf.Environment.
    """
    # 1) load channels + meta
    channels, meta = load_grid(grid_path)
    # 2) create the cost_map (use provided weights or defaults)
    weights = weights or [1.0] * channels.shape[0]
    cost_map = aggregate_cost(channels, weights, smooth_sigma=kwargs.get("smooth_sigma", 1.0))
    start = meta.get("start", (0, 0))
    goal = meta.get("goal", (channels.shape[1] - 1, channels.shape[2] - 1))

    # 3) return a callable or object that constructs your env for each rollout
    # Simple: return a function that returns a new DynamicOceanEnv instance
    def env_factory(**env_kwargs):
        return DynamicOceanEnv(cost_map=cost_map, start=start, goal=goal, **env_kwargs)

    return env_factory
