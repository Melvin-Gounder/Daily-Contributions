# Weighted Interval Scheduling

Dynamic programming with binary-search predecessors selects a maximum-value set of non-overlapping jobs. Half-open intervals permit adjacent jobs. O(n log n) time, O(n) space.

## Run

Python 3.10+; no third-party dependencies.

    cd projects/2026-11-09-weighted-intervals
    python schedule.py
    python -m unittest -v test_schedule.py

## Engineering notes

The implementation is self-contained and intended for learning and extension. Tests cover boundary conditions, invalid inputs, and core behavior. Read the source docstrings for API details.
