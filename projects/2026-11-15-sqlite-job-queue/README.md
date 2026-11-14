# SQLite Leased Job Queue

Durable queue with atomic claims, visibility timeouts, acknowledgements and expired-lease recovery.

## Run

Python 3.9+; standard library only.

```sh
cd projects/2026-11-15-sqlite-job-queue
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Durable queue with atomic claims, visibility timeouts, acknowledgements and expired-lease recovery. Educational implementation with deterministic unit tests. Not hardened for untrusted workloads or large inputs; validate concurrency and performance before production use.
