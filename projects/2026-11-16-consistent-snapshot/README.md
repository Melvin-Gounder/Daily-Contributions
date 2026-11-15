# MVCC Snapshot Key-Value Store

In-memory multi-version key-value store supporting immutable read snapshots, tombstones, and monotonic revision tracking.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py
python -m unittest -v test_tool.py
```

## Design and complexity

Versions are append-only and indexed by monotonically increasing revisions. Binary search makes a single-key snapshot lookup O(log versions); scan is O(keys × log versions). No persistence, transaction isolation, or garbage collection.

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
