# Bellman–Ford Route Analyzer

Shortest paths with negative edges, predecessor reconstruction, and reachable negative-cycle detection.

## Usage and design

Run `python tool.py` for a demo or `python -m unittest -v test_tool.py` for tests. Python 3.9+, standard library only. Time O(VE), memory O(V+E). Negative edges are supported; reachable negative cycles raise ValueError. Unreachable destinations have infinite distance and no path.
