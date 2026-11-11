# Streaming JSONL Deduplication CLI

Line-oriented JSON deduplication by nested field, deterministic first-seen retention, strict errors, and atomic output replacement.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-12-jsonl-deduplication-cli
python dedup.py
python -m unittest -v test_dedup.py
```

## Design and limitations

The module is independently importable; the demonstration is guarded by `__main__`. Tests exercise normal and invalid inputs. This is an educational implementation, not a drop-in production service. Review resource limits, error handling, and threat models before deploying. See the module docstrings for the exact API and behavior.
