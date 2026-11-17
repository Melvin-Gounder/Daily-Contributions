# Merkle Inclusion Proof Toolkit

Domain-separated SHA-256 Merkle roots and verifiable inclusion proofs.

## Usage

Python 3.9+, standard library only. Run `python tool.py` for a demo and `python -m unittest -v test_tool.py` for tests.

## Design and limitations

Merkle tree duplicates odd leaves. 0x00 prefixes leaf hashes, 0x01 prefixes internal hashes. O(n) construction, O(log n) proof and verification. A trusted root is essential; this is not a blockchain protocol.
