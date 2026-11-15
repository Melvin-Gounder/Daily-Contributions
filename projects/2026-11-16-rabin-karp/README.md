# Rabin–Karp Multi-Match Search

Rolling-hash substring search with collision verification, overlapping matches, and Unicode-safe character handling.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py
python -m unittest -v test_tool.py
```

## Design and complexity

Rolling updates take O(1) per window. Candidate matches are verified against the original text, ensuring correctness even with collisions. Expected O(n+m), worst-case O(nm) when collisions are frequent.

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
