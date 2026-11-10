# Streaming K-Way Merge CLI

Heap-based merge of sorted integer streams with input-order validation and atomic output.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-external-merge
python merge.py
python -m unittest -v test_merge.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. Input streams must already be sorted; each is validated during streaming. The merge uses O(k) heap space for k inputs.
