# Bipartite Assignment Matcher

Augmenting-path maximum bipartite matching with deterministic traversal and minimum vertex cover certificate.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-bipartite-matching
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Uses DFS augmenting paths in O(VE) worst case. The minimum vertex cover is derived by alternating reachability (Kőnig's theorem).

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
