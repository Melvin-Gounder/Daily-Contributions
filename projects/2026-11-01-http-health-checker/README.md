# Concurrent HTTP Health Checker

A standard-library Python CLI for checking multiple HTTP endpoints concurrently and turning the results into useful availability and latency metrics.

## What it demonstrates

- bounded concurrency with `ThreadPoolExecutor` for I/O-bound work;
- explicit request timeouts so a slow endpoint cannot block forever;
- HTTP errors and network failures represented as data instead of crashing the batch;
- deterministic output order even though requests finish out of order;
- median latency, which is less sensitive to a single slow outlier than the mean;
- machine-readable JSON output for scripts and monitoring pipelines;
- meaningful process exit codes: `0` only when every endpoint is healthy;
- dependency-free unit tests that mock network I/O.

## Run

Requires Python 3.10+.

```bash
cd projects/2026-11-01-http-health-checker
python health_checker.py https://example.com https://www.python.org
python health_checker.py --timeout 2 --workers 8 --json https://example.com https://www.python.org
```

A failed endpoint makes the process exit with status 1, which is useful in shell scripts and CI jobs.

## Tests

The tests never access the public internet:

```bash
python -m unittest -v test_health_checker.py
```

Seven tests cover successful responses, HTTP failures, network failures, summary calculations, empty input summaries, invalid concurrency configuration, and preservation of input order under concurrency.

## Design notes

HTTP checks are I/O-bound: most wall-clock time is spent waiting on sockets, so a small thread pool can reduce total batch latency without requiring asynchronous-framework dependencies. The worker limit provides backpressure; creating one thread per URL would scale poorly for a large list.

A `2xx` or `3xx` response is considered healthy. Whether redirects should count as healthy is service-specific, so production monitoring might make this configurable. The checker reads one response byte to verify that the response stream is usable while avoiding unnecessary body downloads.

This is an availability probe, not a load tester. Use conservative worker counts against systems you own or are authorized to monitor.

## Complexity

For `n` URLs, result storage is O(n). CPU-side bookkeeping is O(n), while wall-clock duration is dominated by network latency and is approximately the work distributed across at most `workers` concurrent requests. Median calculation is O(h log h) for `h` healthy results in Python's standard-library implementation.
