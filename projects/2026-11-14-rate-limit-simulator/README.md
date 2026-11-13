# Token Bucket Rate Limiter

Deterministic token-bucket admission control with injectable monotonic clock and retry-after calculations.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-rate-limit-simulator
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Single-process non-thread-safe model; O(1) admission, floating-point retry estimates; inject a monotonic clock for tests.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
