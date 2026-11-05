# Circuit Breaker for Resilient Service Calls

A complete synchronous circuit breaker implementing closed → open → half-open → closed. A failure threshold opens the circuit; subsequent calls fail fast. After a configurable cooldown, one probe checks recovery.

Run `python breaker.py` and `python -m unittest discover -v` (Python 3.9+, no dependencies). Tests use an injected clock and never sleep.

Each call adds O(1) state and O(1) overhead. This version is single-threaded; concurrent callers require synchronization to ensure only one half-open probe. This protects dependencies from failure cascades but does not retry requests; callers should account for idempotency and timeouts.
