# A* Grid Pathfinding

Shortest paths on a rectangular binary grid (0=open, 1=wall). Only four cardinal moves, each costing one. Returns a list of coordinates and total cost; unreachable targets return `([], None)`.

Run: `python astar.py` and `python -m unittest -v test_astar.py` from this directory. No dependencies beyond Python 3.

A* orders candidates by distance traveled plus Manhattan distance to the goal. Manhattan distance is consistent and never overestimates the cost of cardinal moves, ensuring optimality. Stale heap entries are ignored. For V cells and E neighbor edges, time O((V+E) log V), memory O(V). Not intended for diagonal or weighted motion.
