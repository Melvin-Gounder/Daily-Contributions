# Strongly Connected Components Analyzer

Tarjan's linear-time graph decomposition, condensation DAG, and cycle identification.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-tarjan-scc
python scc.py
python -m unittest -v test_scc.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. Uses recursive depth-first search, so very deep graphs may exceed Python recursion depth.
