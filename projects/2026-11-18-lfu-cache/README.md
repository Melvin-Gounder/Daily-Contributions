# LFU Cache with LRU Tie-Breaking

Expected constant-time bounded cache with frequency-based eviction and recency tie-breaking.

## Usage

Python 3.9+, standard library only. Run `python tool.py` for a demo and `python -m unittest -v test_tool.py` for tests.

## Design and limitations

Hash maps and ordered buckets give expected O(1) get, update and eviction, O(capacity) storage. Updates count as accesses. Not thread-safe; frequencies are not aged.
