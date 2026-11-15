# Memory-Bounded External Merge Sort

External integer sorting CLI using sorted disk runs and heap-based multiway merge, with cleanup and malformed-input checks.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py unsorted.txt sorted.txt --chunk-size 1000
python -m unittest -v test_tool.py
```

## Design and complexity

Sorts chunks of at most chunk_size integers and merges temporary runs with a heap. Memory is O(chunk_size + number_of_runs), not strictly bounded independent of file size; file-descriptor use grows with run count. Destination is replaced atomically after success.

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
