# Bloom Filter Membership Lab

A Bloom filter answers **definitely not present** or **possibly present** using a compact bit array and SHA-256 double hashing. Useful as a front-end to caches and databases to avoid unnecessary negative lookups.

## Run
```sh
cd projects/2026-11-07-bloom-filter
python bloom.py
python -m unittest -v
```

For capacity `n` and target false-positive rate `p`, allocate approximately `m = -n ln(p)/(ln 2)^2` bits and `k = (m/n) ln 2` hashes. Query and insert cost O(k); storage O(m) bits. `to_json` / `from_json` persist the bitset with base64.

## Limitations
Cannot enumerate items or remove them safely; inserting beyond designed capacity raises false-positive probability. Hashes are not keyed, so this is **not** an authorization or security boundary. JSON is validated for basic bounds but should not be treated as trusted cryptographic data.
