# Consistent Hashing with Virtual Nodes

A runnable SHA-256 consistent-hash ring for assigning keys to distributed cache nodes. Supports node joins/leaves and stable key ownership; tests verify that removing a node only remaps keys that belonged to it.

Run `python ring.py` and `python -m unittest discover -v` inside this directory (Python 3.9+, standard library only).

Each physical node owns 64 virtual points by default to smooth distribution. A key maps clockwise to the next point. Lookup costs O(log V) with binary search, while insertion and deletion cost O(V) due to Python list shifts. Membership and replica count must be identical across clients. This is a teaching implementation, not a consensus protocol.
