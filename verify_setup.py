"""Verification script for Prime Hub setup."""

import sys
import os

print("=" * 60)
print("PRIME INTELLECT HUB - SETUP VERIFICATION")
print("=" * 60)

# Test 1: Import main package
print("\n[1/4] Testing dynamic_ocean package import...")
try:
    import dynamic_ocean
    print(f"    [OK] Package imported from: {dynamic_ocean.__file__}")
except Exception as e:
    print(f"    [FAIL] {e}")
    sys.exit(1)

# Test 2: Import environment class
print("\n[2/4] Testing DynamicOceanEnv import...")
try:
    from dynamic_ocean.envs import DynamicOceanEnv
    print(f"    [OK] DynamicOceanEnv imported successfully")
except Exception as e:
    print(f"    [FAIL] {e}")
    sys.exit(1)

# Test 3: Test environment loader
print("\n[3/4] Testing environment loader...")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "environments", "dynamic-ocean-fields"))
    from load_environment import load_environment
    env_factory = load_environment()
    env = env_factory()
    obs, info = env.reset()
    print(f"    [OK] Environment created and reset successfully")
    print(f"    [OK] Observation keys: {list(obs.keys())}")
    print(f"    [OK] Action space: {env.action_space}")
    env.close()
except Exception as e:
    print(f"    [FAIL] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check required files
print("\n[4/4] Checking required files...")
required_files = [
    "pyproject.toml",
    "dynamic_ocean/__init__.py",
    "environments/dynamic-ocean-fields/load_environment.py",
    "environments/dynamic-ocean-fields/pyproject.toml",
    "environments/dynamic-ocean-fields/README.md",
]

all_exist = True
for file_path in required_files:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        print(f"    [OK] {file_path}")
    else:
        print(f"    [MISSING] {file_path}")
        all_exist = False

if not all_exist:
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] ALL CHECKS PASSED - READY FOR PRIME HUB!")
print("=" * 60)
print("\nNext steps:")
print("1. cd environments\\dynamic-ocean-fields")
print("2. prime login")
print("3. prime env push")
print("\nSee PRIME_HUB_READY.md for detailed instructions.")
