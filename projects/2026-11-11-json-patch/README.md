# Transactional JSON Patch Engine

RFC 6902-inspired add, remove, replace, test operations with JSON Pointer decoding and atomic application.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-json-patch
python patch.py
python -m unittest -v test_patch.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. Supports four JSON Patch operations; move and copy are intentionally out of scope. Failures leave the caller's original document unchanged.
