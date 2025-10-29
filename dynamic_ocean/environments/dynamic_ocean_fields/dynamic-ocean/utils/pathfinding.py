# utils/pathfinding.py
"""
Simple pathfinding utilities: A* and Dijkstra adapted to grid cost maps.

We provide:
- dijkstra_grid(cost_map, start, goal)
- astar_grid(cost_map, start, goal, heuristic='manhattan')
"""

import heapq
import math
from typing import Tuple, List, Optional
import numpy as np

# 8-neighborhood: (dr,dc,move_cost_multiplier)
NEIGHBORS = [
    (-1, 0, 1.0),
    (1, 0, 1.0),
    (0, -1, 1.0),
    (0, 1, 1.0),
    (-1, -1, math.sqrt(2)),
    (-1, 1, math.sqrt(2)),
    (1, -1, math.sqrt(2)),
    (1, 1, math.sqrt(2)),
]


def _reconstruct(prev, start, goal):
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()
    return path


def dijkstra_grid(cost_map: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int]):
    H, W = cost_map.shape
    INF = float("inf")
    dist = np.full((H, W), INF, dtype=float)
    visited = np.zeros((H, W), dtype=bool)
    prev = {}
    sr, sc = start
    gr, gc = goal
    dist[sr, sc] = 0.0
    heap = [(0.0, (sr, sc))]
    while heap:
        d, (r, c) = heapq.heappop(heap)
        if visited[r, c]:
            continue
        visited[r, c] = True
        if (r, c) == (gr, gc):
            break
        for dr, dc, mult in NEIGHBORS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < H and 0 <= nc < W):
                continue
            # move cost: mult * average cell cost
            move_cost = mult * 0.5 * (cost_map[r, c] + cost_map[nr, nc])
            nd = d + move_cost
            if nd < dist[nr, nc]:
                dist[nr, nc] = nd
                prev[(nr, nc)] = (r, c)
                heapq.heappush(heap, (nd, (nr, nc)))
    if not visited[gr, gc]:
        return None, float("inf")
    path = _reconstruct(prev, (sr, sc), (gr, gc))
    return path, dist[gr, gc]


def astar_grid(cost_map: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int], heuristic: str = "manhattan"):
    H, W = cost_map.shape
    def h(a, b):
        (r1, c1), (r2, c2) = a, b
        if heuristic == "manhattan":
            return abs(r1 - r2) + abs(c1 - c2)
        elif heuristic == "euclidean":
            return math.hypot(r1 - r2, c1 - c2)
        else:
            return 0.0

    g_score = {start: 0.0}
    f_score = {start: h(start, goal)}
    open_heap = [(f_score[start], start)]
    prev = {}
    closed = set()

    while open_heap:
        f, current = heapq.heappop(open_heap)
        if current == goal:
            path = _reconstruct(prev, start, goal)
            return path, g_score[goal]
        if current in closed:
            continue
        closed.add(current)
        r, c = current
        for dr, dc, mult in NEIGHBORS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < H and 0 <= nc < W):
                continue
            tentative_g = g_score[current] + mult * 0.5 * (cost_map[r, c] + cost_map[nr, nc])
            neighbor = (nr, nc)
            if tentative_g < g_score.get(neighbor, float("inf")):
                prev[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor, goal)
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))
    return None, float("inf")
