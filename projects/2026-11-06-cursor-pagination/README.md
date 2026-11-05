# Signed Keyset Pagination

Demonstrates cursor-based API pagination without fragile offset positions. Cursors contain the last returned integer ID and are authenticated with HMAC-SHA256, so clients cannot silently change the position.

Run `python cursor.py` and `python -m unittest discover -v` (Python 3.9+, no dependencies). Tests cover full traversal, tampering, wrong keys, sorting, and empty data.

**Security:** HMAC provides integrity, not secrecy. Use a securely generated key, bind tokens to the requesting user and query filters, and add expiration and key rotation in production. The in-memory example scans O(n) per page; a real indexed database can use `WHERE id > ? ORDER BY id LIMIT ?` for approximately O(log n + page_size) retrieval.
