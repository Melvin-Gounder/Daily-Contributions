# Streaming CSV Schema Profiler

Incremental CSV column statistics, null counts, numeric inference, and bounded distinct-value sampling.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-csv-schema-profiler
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Reads one row at a time, retaining bounded examples per column; numeric inference is conservative and finite-only.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
