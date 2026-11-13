# DAG Transitive Reduction

Removes redundant directed edges while preserving reachability; rejects cyclic input.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-dag-transitive-reduction
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Only DAGs have a unique transitive reduction. Straightforward reachability checks favor clarity over optimal asymptotic performance.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
