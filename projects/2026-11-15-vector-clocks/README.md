# Vector Clock Causality Toolkit

Logical clocks for distributed events, message merges, happens-before and concurrent-event detection.

## Usage

Python 3.9+; Python standard library only.

```sh
cd projects/2026-11-15-vector-clocks
python tool.py
python -m unittest -v test_tool.py
```

## Design

Logical clocks for distributed events, message merges, happens-before and concurrent-event detection. Designed as an educational, dependency-free implementation with deterministic unit tests and explicit input checks.

## Limitations

Small-scale demonstration, not a production service. Review concurrency, security, performance, and input limits before deployment.
