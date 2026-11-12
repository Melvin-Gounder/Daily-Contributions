# Weighted Quantile Calculator

Exact rational weighted quantiles, strict validation, deterministic ordering and boundary behavior.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-weighted-quantiles
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Returns the smallest observed value whose cumulative weight reaches the requested quantile; this is a discrete inverse-CDF definition, not interpolated sample quantiles.

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
