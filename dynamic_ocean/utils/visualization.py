# utils/visualization.py
"""
Visualization helpers for cost maps and planned paths.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple


def plot_cost_map(cost_map: np.ndarray, path: List[Tuple[int, int]] = None, start=None, goal=None, cmap="viridis"):
    """
    Plot cost map (H,W) and overlay path as sequence of (r,c).
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(cost_map, origin="lower", cmap=cmap)
    plt.colorbar(label="cost")
    if path is not None and len(path) > 0:
        rows = [p[0] for p in path]
        cols = [p[1] for p in path]
        plt.plot(cols, rows, color="white", linewidth=2, label="path")
        plt.scatter(cols[0], rows[0], c="green", marker="o", s=60, label="start")
        plt.scatter(cols[-1], rows[-1], c="red", marker="X", s=60, label="goal")
    elif start is not None and goal is not None:
        plt.scatter(start[1], start[0], c="green", marker="o", s=60, label="start")
        plt.scatter(goal[1], goal[0], c="red", marker="X", s=60, label="goal")
    plt.legend()
    plt.title("Cost map with planned path")
    plt.show()
