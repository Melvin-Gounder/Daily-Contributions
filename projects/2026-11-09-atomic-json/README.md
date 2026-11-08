# Atomic JSON Settings Store

Crash-conscious atomic file replacement using temporary files and fsync; revision checks detect stale sequential writes. Not safe for concurrent cross-process writers without locks.

## Run

Python 3.10+; no third-party dependencies.

    cd projects/2026-11-09-atomic-json
    python store.py
    python -m unittest -v test_store.py

## Engineering notes

The implementation is self-contained and intended for learning and extension. Tests cover boundary conditions, invalid inputs, and core behavior. Read the source docstrings for API details.
