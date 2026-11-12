# Unicode Edit Distance and Alignment

Wagner–Fischer dynamic programming with deterministic insert/delete/substitute alignment and replay.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-edit-distance
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

O(nm) time and memory; alignment is deterministic but not unique. Unicode comparisons operate on code points, not grapheme clusters.

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
