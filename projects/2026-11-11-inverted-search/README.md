# Ranked Full-Text Search Index

BM25 ranking with token normalization, document replacement, and explainable term scores.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-inverted-search
python search.py
python -m unittest -v test_search.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. BM25 ranks matching documents but does not provide stemming, phrase search, or persistence.
