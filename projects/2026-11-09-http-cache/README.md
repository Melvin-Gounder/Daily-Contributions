# HTTP Cache Freshness Model

Pure HTTP Cache-Control educational model for max-age, s-maxage, private, public, no-store, no-cache, and authenticated shared caches. Omits Date/Age corrections, Vary, validators, and other RFC 9111 rules; not production HTTP cache.

## Run

Python 3.10+; no third-party dependencies.

    cd projects/2026-11-09-http-cache
    python cache.py
    python -m unittest -v test_cache.py

## Engineering notes

The implementation is self-contained and intended for learning and extension. Tests cover boundary conditions, invalid inputs, and core behavior. Read the source docstrings for API details.
