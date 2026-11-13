# Smooth Weighted Round Robin

Smooth weighted scheduling with deterministic tie-breaking and runtime weight updates.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-weighted-round-robin
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

O(number of destinations) per selection, single-threaded. Stable dictionary insertion order determines ties.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
