# Bloom Filter Membership Laboratory

Configurable probabilistic set membership with deterministic double hashing, capacity estimates, and serialization.

## Usage and design

Run `python tool.py` or `python -m unittest -v test_tool.py`. Python 3.9+; no dependencies. The filter uses SHA-256 double hashing and an approximate optimal bit count/hash count. Insert and membership cost O(k); memory O(m) bits. False positives are possible, deletions are deliberately unsupported, and serialization is not authenticated. Use only for non-security-critical prefiltering.
