"""Quick test script for load_environment."""

from load_environment import load_environment

# Test 1: Load with defaults
print("Test 1: Loading environment with defaults...")
env = load_environment()
print(f"  Environment: {type(env).__name__}")
print(f"  Action space: {env.action_space}")
print(f"  Cost map shape: {env.cost_map.shape}")

# Test 2: Reset and step
print("\nTest 2: Reset and step...")
obs, info = env.reset()
print(f"  Observation keys: {list(obs.keys())}")
print(f"  Agent start: {tuple(obs['agent_pos'])}")
print(f"  Goal: {tuple(obs['goal_pos'])}")

action = env.action_space.sample()
obs, reward, done, truncated, info = env.step(action)
print(f"  Step result - reward: {reward:.3f}, done: {done}")

# Test 3: Custom grid size
print("\nTest 3: Custom grid size...")
env2 = load_environment(grid_size=(10, 10), start=(0, 0), goal=(9, 9))
print(f"  Cost map shape: {env2.cost_map.shape}")

print("\nAll tests passed!")
