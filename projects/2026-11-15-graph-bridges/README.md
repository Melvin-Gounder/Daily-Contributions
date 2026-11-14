# Graph Bridges and Articulation Points

Tarjan low-link traversal for critical undirected edges and vertices across disconnected graphs.

## Run

Python 3.9+; standard library only.

```sh
cd projects/2026-11-15-graph-bridges
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Tarjan low-link traversal for critical undirected edges and vertices across disconnected graphs. Educational implementation with deterministic unit tests. Not hardened for untrusted workloads or large inputs; validate concurrency and performance before production use.
