# Merkle Tree Integrity Proofs

Build a Merkle tree from ordered byte records, publish a root, and verify a record's membership using a compact sibling proof. Leaf and internal-node hashes have different prefixes, and odd layers duplicate the final node.

Run `python merkle.py` and `python -m unittest discover -v` (Python 3.9+, standard library). Tests cover 1–8 leaves, tampering, ordering, and invalid inputs.

Building the tree takes O(n) hashes and O(n) memory; proof size and verification work are O(log n). **Security caveat:** the claimed root must be obtained from a trusted channel. This does not prove that a batch is complete or that its publisher is honest.
