# Lazy Segment Tree for Range Updates

Logarithmic range-add and range-sum operations with lazy propagation, input validation and deterministic tests.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py
python -m unittest -v test_tool.py
```

## Design and complexity

Half-open intervals [left,right). Build O(n), updates and queries O(log n), storage O(n). Lazy tags defer propagation until a descendant is visited.

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
