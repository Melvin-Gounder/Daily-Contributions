# Weighted Trie Autocomplete Engine

Prefix search with ranked suggestions, updates, deletion, and deterministic tie-breaking.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-trie-autocomplete
python trie.py
python -m unittest -v test_trie.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. Prefix traversal is O(prefix length + number of matching trie nodes), with full candidate sorting.
