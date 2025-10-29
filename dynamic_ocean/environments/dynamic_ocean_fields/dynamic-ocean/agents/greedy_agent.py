# agents/greedy_agent.py
"""
Greedy agent: at each step, inspect the local_patch in the observation and pick the neighboring cell
with the lowest cost. Falls back to random if ties or issues.
"""

import numpy as np
from typing import Any
import random

# Import MOVES mapping from envs if necessary; replicate small map here:
MOVES = {
    0: (0, 0),    # stay
    1: (-1, 0),   # N
    2: (-1, 1),   # NE
    3: (0, 1),    # E
    4: (1, 1),    # SE
    5: (1, 0),    # S
    6: (1, -1),   # SW
    7: (0, -1),   # W
    8: (-1, -1),  # NW
}


class GreedyAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, obs) -> Any:
        """
        obs['local_patch'] shape: (1, K, K)
        obs['agent_pos'] and goal are also available if needed.
        Strategy: choose the move that points to the lowest-cost cell within the local patch.
        """
        patch = obs["local_patch"][0]  # (K, K)
        K = patch.shape[0]
        center = K // 2
        best_actions = []
        best_cost = float("inf")
        for act, (dr, dc) in MOVES.items():
            nr = center + dr
            nc = center + dc
            if 0 <= nr < K and 0 <= nc < K:
                c = float(patch[nr, nc])
                if c < best_cost:
                    best_cost = c
                    best_actions = [act]
                elif c == best_cost:
                    best_actions.append(act)
        if not best_actions:
            return self.action_space.sample()
        return random.choice(best_actions)

    def reset(self):
        pass
