# SQLite Idempotent Command Handler

Transactional request-key deduplication with payload fingerprints, durable responses and conflict rejection.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-sqlite-idempotency
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Atomicity relies on SQLite transactions. Use a dedicated connection per concurrent worker and enforce unique request keys at the database level.

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
