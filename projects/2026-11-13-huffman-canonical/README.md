# Canonical Huffman Codebook

Deterministic Huffman length construction and canonical prefix-code assignment with round-trip bit encoding.

## Run

Python 3.9+, standard library only.

```sh
cd projects/2026-11-13-huffman-canonical
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Heap construction O(k log k); canonical code ordering uses (length, symbol).

The module is importable; tests cover normal and boundary cases. Educational implementation, not production-hardened.
