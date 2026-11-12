# Bounded Streaming Top-K Leaderboard

Memory-bounded top-k aggregation over scored records with deterministic tie-breaking and input validation.

## Run

Python 3.9+, standard library only.

```sh
cd projects/2026-11-13-topk-stream
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

O(n log k) time and O(k) memory; ties favor earlier input.

The module is importable; tests cover normal and boundary cases. Educational implementation, not production-hardened.
