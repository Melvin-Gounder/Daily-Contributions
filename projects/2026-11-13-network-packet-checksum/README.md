# Internet Checksum Laboratory

RFC 1071 one's-complement checksum calculation and verification for arbitrary byte sequences.

## Run

Python 3.9+, standard library only.

```sh
cd projects/2026-11-13-network-packet-checksum
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Odd-length inputs are padded with zero for calculation. This checksum detects accidental errors, not malicious tampering.

The module is importable; tests cover normal and boundary cases. Educational implementation, not production-hardened.
