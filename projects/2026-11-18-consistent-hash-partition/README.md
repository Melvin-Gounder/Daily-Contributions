# Jump Consistent Hash Partitioning

Constant-space stable partition assignment with deterministic 64-bit jump consistent hashing.

## Usage

Python 3.9+, standard library only. Run `python tool.py` for a demo and `python -m unittest -v test_tool.py` for tests.

## Design and limitations

Jump consistent hashing (Lamping–Veach) takes expected O(log buckets) time and O(1) extra space. Unlike ring hashing, buckets are integer IDs and growth should append buckets. SHA-256 converts text keys to stable 64-bit integers.
