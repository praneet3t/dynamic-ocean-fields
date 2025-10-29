# main.py
"""
Entry point for running basic demos:
- generate a sample grid
- compute cost map
- run planner and visualize
- run environment stepping with a greedy baseline
"""

import argparse
from utils.data_loader import generate_random_grid, save_grid, load_grid
from envs.cost_functions import aggregate_cost
from utils.pathfinding import astar_grid
from utils.visualization import plot_cost_map
from envs.dynamic_ocean_env import DynamicOceanEnv
from agents.greedy_agent import GreedyAgent
import numpy as np


def run_demo(args):
    # generate or load grid
    if args.grid_path:
        channels, meta = load_grid(args.grid_path)
    else:
        channels = generate_random_grid(C=args.C, H=args.H, W=args.W, obstacle_prob=args.obst, seed=args.seed)
        save_grid("data/sample_grid.npz", channels, meta={"generated_by": "main_demo", "seed": args.seed})

    weights = args.weights or [1.0] * channels.shape[0]
    cost_map = aggregate_cost(channels, weights, smooth_sigma=args.sigma)

    # plan
    start = (0, 0)
    goal = (channels.shape[1] - 1, channels.shape[2] - 1)
    path, total_cost = astar_grid(cost_map, start, goal)
    print(f"Planned cost: {total_cost}, Path length: {len(path) if path else 'None'}")

    # visualize
    plot_cost_map(cost_map, path=path, start=start, goal=goal)

    # run env with greedy agent
    env = DynamicOceanEnv(cost_map, start, goal, patch_size=3)
    obs, info = env.reset()
    agent = GreedyAgent(env.action_space)
    done = False
    cum_reward = 0.0
    while not done:
        action = agent.act(obs)
        obs, r, done, _, info = env.step(action)
        cum_reward += r
    print("Episode finished. Cumulative reward:", cum_reward)
    print("Info:", info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_path", type=str, default=None, help="Path to .npz grid file")
    parser.add_argument("--C", type=int, default=3)
    parser.add_argument("--H", type=int, default=64)
    parser.add_argument("--W", type=int, default=64)
    parser.add_argument("--obst", type=float, default=0.03)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--weights", nargs="+", type=float, default=None)
    parser.add_argument("--sigma", type=float, default=1.0)
    args = parser.parse_args()
    run_demo(args)
