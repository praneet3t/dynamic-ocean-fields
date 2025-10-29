# agents/random_agent.py
"""
Random baseline agent that samples actions uniformly.
"""

import random
from typing import Any


class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, obs) -> Any:
        return self.action_space.sample()

    def reset(self):
        pass
