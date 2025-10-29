# agents/rl_agent.py
"""
Placeholder RL agent wrapper.

This file provides a thin adapter to plug RL libraries (stable-baselines3, rllib, etc.)
into the eval framework. The class expects a `learned_model` object with a `.predict(obs, deterministic=True)` API,
but defaults to None so it can be used as a scaffold.
"""

from typing import Any


class RLAgent:
    def __init__(self, model=None):
        """
        model: an RL model object that implements `predict(obs, deterministic=True)` returning (action, info)
        """
        self.model = model

    def act(self, obs, deterministic=True) -> Any:
        if self.model is None:
            raise RuntimeError("No model provided to RLAgent")
        action, _ = self.model.predict(obs, deterministic=deterministic)
        return action

    def reset(self):
        if hasattr(self.model, "reset"):
            self.model.reset()
