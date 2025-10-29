# tests/test_env.py
import numpy as np
from envs.dynamic_ocean_env import DynamicOceanEnv
from envs.cost_functions import aggregate_cost

def test_env_basic_run():
    # small 5x5 grid with low costs and a clear path
    H, W = 5, 5
    channels = np.zeros((1, H, W), dtype=float)
    # add obstacle in center
    channels[0, 2, 2] = 10.0
    weights = [1.0]
    cost_map = aggregate_cost(channels, weights)
    start = (0, 0)
    goal = (4, 4)
    env = DynamicOceanEnv(cost_map, start, goal, patch_size=3, max_steps=100)
    obs, info = env.reset()
    assert obs["agent_pos"].tolist() == [0, 0]
    # take a single step (stay)
    obs, r, done, _, info = env.step(0)
    assert "cell_cost" in info
    # ensure stepping into goal works by teleporting agent and computing final reward
    env.agent_pos = np.array(goal)
    obs, r, done, _, info = env.step(0)  # staying on goal should mark done
    assert done is True
