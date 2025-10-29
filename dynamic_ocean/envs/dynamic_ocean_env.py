# envs/dynamic_ocean_env.py
"""
Gymnasium-compatible grid environment for Dynamic Ocean Fields.

Observation:
    - 'local_patch' : numpy array shape (C, K, K) where K is patch size
    - 'agent_pos'   : numpy array shape (2,) (row, col)
    - 'goal_pos'    : numpy array shape (2,) (row, col)

Action space (Discrete(9)):
    0: stay
    1: N, 2: NE, 3: E, 4: SE, 5: S, 6: SW, 7: W, 8: NW

Reward:
    - negative of the cost of the cell moved into (so agents minimize cumulative cost)
Episode ends:
    - agent reaches goal
    - agent exceeds max_steps
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
from typing import Tuple, Optional

# 8-neighborhood moves plus stay
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


class DynamicOceanEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(
        self,
        cost_map: np.ndarray,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        patch_size: int = 3,
        max_steps: Optional[int] = None,
    ):
        """
        Args:
            cost_map: 2D numpy array of shape (H, W) with normalized cell costs (float).
            start: (row, col)
            goal: (row, col)
            patch_size: size of square local observation patch (odd integer, default 3)
            max_steps: maximum allowed steps in episode (defaults to H*W*2)
        """
        assert cost_map.ndim == 2, "cost_map must be 2D"
        assert patch_size % 2 == 1 and patch_size >= 1, "patch_size must be odd >=1"

        self.cost_map = cost_map.astype(float)
        self.H, self.W = self.cost_map.shape
        self.start = tuple(start)
        self.goal = tuple(goal)
        self.patch_size = patch_size
        self.pad = patch_size // 2
        self.max_steps = max_steps or (self.H * self.W * 2)

        # observation spaces
        # local_patch: shape (1, K, K) for now (single-channel cost); can be extended
        self.observation_space = spaces.Dict(
            {
                "local_patch": spaces.Box(
                    low=0.0, high=float("inf"), shape=(1, patch_size, patch_size), dtype=float
                ),
                "agent_pos": spaces.Box(low=0, high=max(self.H, self.W), shape=(2,), dtype=int),
                "goal_pos": spaces.Box(low=0, high=max(self.H, self.W), shape=(2,), dtype=int),
            }
        )

        # action space: 9 discrete actions
        self.action_space = spaces.Discrete(len(MOVES))

        # internal state
        self.agent_pos = None
        self.step_count = None
        self._padded_cost = np.pad(self.cost_map, pad_width=self.pad, mode="edge")
        self.last_reward = 0.0

    def reset(self, seed: Optional[int] = None, options: dict = None):
        super().reset(seed=seed)
        self.agent_pos = np.array(self.start, dtype=int)
        self.step_count = 0
        self.last_reward = 0.0
        obs = self._get_obs()
        info = {"start": self.start, "goal": self.goal}
        return obs, info

    def step(self, action):
        assert self.action_space.contains(action), f"Invalid action {action}"
        dr, dc = MOVES[int(action)]
        nr = int(self.agent_pos[0] + dr)
        nc = int(self.agent_pos[1] + dc)

        # clip to grid boundaries
        nr = int(np.clip(nr, 0, self.H - 1))
        nc = int(np.clip(nc, 0, self.W - 1))

        # move agent
        self.agent_pos = np.array([nr, nc], dtype=int)
        self.step_count += 1

        # reward is negative cost of the entered cell
        cell_cost = float(self.cost_map[nr, nc])
        reward = -cell_cost
        self.last_reward = reward

        done = False
        info = {"cell_cost": cell_cost}
        if (nr, nc) == tuple(self.goal):
            done = True
            info["success"] = True
        elif self.step_count >= self.max_steps:
            done = True
            info["success"] = False

        obs = self._get_obs()
        return obs, reward, done, False, info

    def _get_obs(self):
        r, c = tuple(self.agent_pos)
        # extract patch from padded cost map
        r_p = r + self.pad
        c_p = c + self.pad
        patch = self._padded_cost[r_p - self.pad : r_p + self.pad + 1, c_p - self.pad : c_p + self.pad + 1]
        patch = np.asarray(patch, dtype=float).reshape((1, self.patch_size, self.patch_size))
        obs = {
            "local_patch": patch,
            "agent_pos": np.array(self.agent_pos, dtype=int),
            "goal_pos": np.array(self.goal, dtype=int),
        }
        return obs

    def render(self, mode="human"):
        # Minimal textual render — users should use utils.visualization for plots
        print(f"Step {self.step_count} | Agent: {tuple(self.agent_pos)} | Last reward: {self.last_reward:.4f}")

    def close(self):
        pass
