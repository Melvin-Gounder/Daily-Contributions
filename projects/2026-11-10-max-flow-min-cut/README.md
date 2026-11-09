# Max Flow / Min Cut Explorer

Edmonds–Karp residual-network solver with parallel-edge aggregation, augmenting-path traces, min-cut certificates, and flow conservation tests.

## Run

Requires Python 3.10+ and only the standard library. From this project directory:

```bash
python flow.py
python -m unittest -v test_flow.py
```

## Design and limitations

For V vertices and E edges, Edmonds–Karp is O(V E²) time. Only integer capacities are accepted. The cut certificate's capacity must equal the computed flow. Node identifiers should be hashable; string names give predictable display.

## Learning objectives

Read the implementation and tests together to understand invariants, input validation, boundary cases, and failure behavior. Extend the tests before modifying core logic.
