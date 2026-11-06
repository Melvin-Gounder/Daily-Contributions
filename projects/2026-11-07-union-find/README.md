# Disjoint Set Connectivity Toolkit

A reusable union-find structure with **path compression** and **union by size**. Useful for connectivity in undirected networks, clustering, and detecting cycles during Kruskal's minimum spanning tree algorithm.

## Run
```sh
cd projects/2026-11-07-union-find
python connectivity.py
python -m unittest -v
```

`union(a,b)` returns `False` when already connected. Unknown vertices raise `KeyError`; `add` explicitly registers new ones. `components()` returns sets of connected vertices.

## Complexity
A sequence of `m` union/find operations on `n` items costs O(m α(n)) amortized, where α is the inverse Ackermann function (effectively constant for practical sizes). Storage is O(n). Component enumeration costs O(n α(n)). Edges are processed in their input order, so the redundant-edge list is deterministic.
