# Incremental Build Impact Planner

Reverse-edge affected-target discovery plus deterministic heap-based Kahn topological sorting. Detects cycles and unknown dependencies. O(V+E+V log V) worst-case; models build ordering, not command execution.

## Run

Python 3.10+; no third-party dependencies.

    cd projects/2026-11-09-build-impact
    python planner.py
    python -m unittest -v test_planner.py

## Engineering notes

The implementation is self-contained and intended for learning and extension. Tests cover boundary conditions, invalid inputs, and core behavior. Read the source docstrings for API details.
