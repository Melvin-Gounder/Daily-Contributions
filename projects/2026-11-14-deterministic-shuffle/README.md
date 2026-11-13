# Reproducible Fisher-Yates Shuffle

Seeded Fisher–Yates shuffle, unbiased index selection via rejection sampling, and deterministic replay.

## Run

Python 3.9+; standard library only.

```sh
cd projects/2026-11-14-deterministic-shuffle
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

SHA-256 counter stream is deterministic, not a CSPRNG. Rejection sampling avoids modulo bias; intended for repeatable simulations, not secrets.

The included tests cover representative and error cases; execute them locally before deployment.
