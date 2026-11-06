# Deterministic Retry Policy

A standard-library retry utility for transient network failures. Supports a strict attempt budget, capped exponential backoff, **full jitter**, exception allowlisting, injected clock-independent sleeper, and retry telemetry.

## Run
```sh
cd projects/2026-11-07-retry-backoff
python retry.py
python -m unittest -v
```

Call `run(lambda: fetch(), attempts=4, retry_on=(TimeoutError,))`. Failed attempts sleep; successful attempts and terminal failures never sleep. Inject a fake `sleep` and RNG for deterministic tests.

## Design
For retry number `n`, the upper delay bound is `min(cap, base * 2**(n-1))`; a uniform draw in this range reduces synchronized retries. At most `attempts` operations execute. Memory usage is O(1); runtime includes actual operation and sleep times. Retries are safe only for idempotent operations or operations with idempotency keys; never blindly retry payments.
