# Signed Webhook Verification

A defensive educational protocol: HMAC-SHA256 over `ASCII(timestamp) + "." + raw_request_body`, formatted as `sha256=<hex>`. Verify the **raw bytes before JSON parsing**. The timestamp tolerance rejects stale requests; a per-process cache rejects repeated signatures.

Run `python webhook.py` and `python -m unittest -v test_webhook.py`. No external packages.

Production considerations: use HTTPS, secret management, body-size limits, key rotation, and an atomic shared TTL store for replay prevention across workers. This is not a drop-in implementation of any vendor's webhook scheme. HMAC work is O(B) for body length B; educational cache pruning is O(N) over recently seen signatures.
