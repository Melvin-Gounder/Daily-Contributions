# TTL Cache with Fake Clock

A dependency-free bounded cache combining **time-to-live expiry** with **least-recently-used eviction**. Expiry is fixed relative to the last write (not refreshed by reads). An injected monotonic clock makes boundary cases reproducible.

## Run
```sh
cd projects/2026-11-07-ttl-cache
python ttl_cache.py
python -m unittest -v
```

`put(key, value)`, `get(key, default)`, `delete(key)`, and `len(cache)` form the API. Expired entries are purged before operations. `get` promotes live keys to most-recently-used; writing an existing key refreshes its TTL.

## Complexity and tradeoffs
`get` and `put` perform an O(n) expiry sweep (n <= capacity), with O(1) ordered-map access/eviction. Storage is O(capacity). For high-throughput systems use a min-heap of deadlines for efficient expiry or a background sweeper. This implementation is single-threaded and not persistent.
