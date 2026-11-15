# Banker's Algorithm Safety Analyzer

Deadlock-avoidance safety checking for multi-resource processes with safe sequences and request simulation.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py
python -m unittest -v test_tool.py
```

## Design and complexity

Simulates process completion while enough resources are available, returning a safe sequence when one exists. Requests are evaluated on copies, never mutating caller state. Worst-case O(n²m).

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
