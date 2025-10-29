"""
Utilities to generate sample grids and load saved grids.

Run:
    python -m utils.data_loader --generate-sample --out data/sample_grid.npz
"""

import argparse
import numpy as np
import xarray as xr
from pathlib import Path
from typing import Optional


def generate_random_grid(C=3, H=64, W=64, obstacle_prob=0.03, seed: Optional[int] = None):
    rng = np.random.default_rng(seed)
    channels = rng.random((C, H, W)).astype(float)
    # Make last channel an obstacle-ish map if C >=1
    if C >= 1:
        obst = (rng.random((H, W)) < obstacle_prob).astype(float)
        channels[-1] = obst * 10.0  # amplify obstacle measure
    return channels


def save_grid(path: str, channels: np.ndarray, meta: dict = None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if meta is None:
        meta = {}
    np.savez_compressed(path, channels=channels, meta=meta)


def load_grid(path: str):
    data = np.load(path, allow_pickle=True)
    channels = data["channels"]
    meta = data.get("meta", {})
    if hasattr(meta, "item"):
        meta = meta.item()
    return channels, meta


def convert_netcdf_to_grid(nc_path: str, varnames: list, time_index: int = 0):
    """
    Convert a netCDF (xarray) with lat/lon grid into a simple (C,H,W) array.
    - varnames: list of variable names to extract (e.g. ['hs','current_mag'])
    - time_index: index along the time dimension to take a single snapshot
    Note: This is intentionally simple. For production you should handle regridding and projections.
    """
    ds = xr.open_dataset(nc_path)
    channels = []
    for var in varnames:
        if var not in ds:
            raise KeyError(f"{var} not in {nc_path}")
        arr = ds[var].isel(time=time_index).values.astype(float)
        channels.append(arr)
    channels = np.stack(channels, axis=0)
    return channels


def _cli():
    parser = argparse.ArgumentParser(description="Data loader for dynamic-ocean-fields hub")
    parser.add_argument("--generate-sample", action="store_true", help="Generate a random sample grid")
    parser.add_argument("--out", type=str, default="data/sample_grid.npz", help="Output path")
    parser.add_argument("--C", type=int, default=3, help="Number of channels")
    parser.add_argument("--H", type=int, default=64, help="Height")
    parser.add_argument("--W", type=int, default=64, help="Width")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--obst", type=float, default=0.03, help="Obstacle probability")
    args = parser.parse_args()

    if args.generate_sample:
        ch = generate_random_grid(C=args.C, H=args.H, W=args.W, obstacle_prob=args.obst, seed=args.seed)
        save_grid(args.out, ch, meta={"generated_by": "data_loader", "seed": args.seed})
        print(f"Saved sample grid to {args.out}")


if __name__ == "__main__":
    _cli()
