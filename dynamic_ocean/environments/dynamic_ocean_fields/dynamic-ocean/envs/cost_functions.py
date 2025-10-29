# envs/cost_functions.py
"""
Cost aggregation utilities.

- normalize_channel: robust min-max normalization with percentile clipping
- aggregate_cost: apply per-channel transforms, normalize, weight, and sum
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from typing import Callable, Iterable, List, Optional


def normalize_channel(
    ch: np.ndarray, clip_percentiles: Optional[tuple] = (1, 99)
) -> np.ndarray:
    """
    Normalize channel to [0,1] using robust min-max with percentile clipping.

    Args:
        ch: 2D array
        clip_percentiles: (low_pct, high_pct) - if None, use min/max

    Returns:
        normalized channel
    """
    ch = np.asarray(ch, dtype=float)
    if clip_percentiles is not None:
        lo = np.nanpercentile(ch, clip_percentiles[0])
        hi = np.nanpercentile(ch, clip_percentiles[1])
    else:
        lo = np.nanmin(ch)
        hi = np.nanmax(ch)
    if np.isclose(hi, lo):
        return np.zeros_like(ch)
    norm = (ch - lo) / (hi - lo)
    norm = np.clip(norm, 0.0, 1.0)
    return norm


def aggregate_cost(
    channels: np.ndarray,
    weights: Iterable[float],
    transforms: Optional[Iterable[Callable[[np.ndarray], np.ndarray]]] = None,
    smooth_sigma: float = 0.0,
) -> np.ndarray:
    """
    Aggregate multi-channel cost into a single 2D cost map.

    Args:
        channels: array shaped (C, H, W)
        weights: length-C iterable of non-negative weights
        transforms: optional list of per-channel transform functions
        smooth_sigma: gaussian smoothing sigma to apply at the end (0 => no smoothing)

    Returns:
        cost_map: 2D array shaped (H, W) normalized to ~[0, sum(weights)]
    """
    channels = np.asarray(channels)
    assert channels.ndim == 3, "channels must be shape (C, H, W)"
    C, H, W = channels.shape
    weights = list(weights)
    assert len(weights) == C, "weights length must match channel count"

    if transforms is None:
        transforms = [lambda x: x for _ in range(C)]
    else:
        transforms = list(transforms)
        assert len(transforms) == C

    normed = []
    for i in range(C):
        ch = transforms[i](channels[i])
        chn = normalize_channel(ch)
        normed.append(chn * weights[i])

    cost = np.sum(normed, axis=0)
    if smooth_sigma and smooth_sigma > 0.0:
        cost = gaussian_filter(cost, sigma=smooth_sigma)

    # optional re-normalize to [0,1] for stability
    if np.nanmax(cost) > 0:
        cost = cost / float(np.nanmax(cost))

    return cost
