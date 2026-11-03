# Dijkstra Route Planner

Run `python routes.py` for a sample road network and `python -m unittest -v test_routes.py` for tests. Represent a directed graph as `{"A": {"B": 4}, "B": {}}`; undirected roads require an edge in both directions.

The min-heap expands the cheapest tentative route, and the result records the distance and actual path to each vertex. Equal-cost routes use lexicographically smaller node sequences for reproducibility. Negative, infinite, and NaN weights are rejected because Dijkstra's algorithm assumes nonnegative costs. Unreachable nodes return infinite distance and no path. With path tuples stored in the heap, this educational implementation may use additional memory/time beyond the usual O((V+E) log V) distance-only implementation; use predecessor pointers for very large graphs. Node names should be strings.
