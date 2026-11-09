# Safe ZIP Extraction CLI

ZIP archive extraction with path traversal rejection, symlink rejection, duplicate-output checks, per-file and aggregate size budgets, and isolated tests.

## Run

Requires Python 3.10+ and only the standard library. From this project directory:

```bash
python safezip.py
python -m unittest -v test_safezip.py
```

## Design and limitations

Designed for a single trusted process, not a hostile concurrent writer: an attacker changing destination paths concurrently could race checks. Extraction is not transactional; failures may leave partial output. CRC errors propagate. Always use a dedicated empty destination.

## Learning objectives

Read the implementation and tests together to understand invariants, input validation, boundary cases, and failure behavior. Extend the tests before modifying core logic.
