# Structured Log Redaction Filter

Recursive secret redaction for JSON-like events with case-insensitive keys, cycle detection and immutable output.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-log-redaction
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Key-based redaction is not a complete DLP solution: sensitive values under innocuous keys remain visible. Apply before log emission.

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
