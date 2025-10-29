# tests/test_costs.py
import numpy as np
from envs.cost_functions import normalize_channel, aggregate_cost

def test_normalize_channel_constant():
    a = np.ones((4,4)) * 5.0
    n = normalize_channel(a)
    assert n.max() == 0.0 and n.min() == 0.0  # constant channel maps to zeros

def test_aggregate_cost_shapes():
    C, H, W = 3, 8, 8
    channels = np.random.RandomState(0).rand(C, H, W)
    weights = [1.0, 0.5, 2.0]
    cost = aggregate_cost(channels, weights)
    assert cost.shape == (H, W)
    assert (cost >= 0.0).all()
