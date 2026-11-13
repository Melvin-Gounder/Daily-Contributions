# Disjoint Interval Set

Normalized half-open integer interval unions, intersection, subtraction, and membership.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-interval-set
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Intervals use [start,end); merging is O(n log n), membership O(log n). Difference is O(nm) in this educational implementation.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
