# Password Hashing Lab

Run `python passwords.py` for a demo, and `python -m unittest -v test_passwords.py` for tests. This project demonstrates **one-way password storage**, not encryption: each password receives a cryptographically random 16-byte salt and a PBKDF2-HMAC-SHA256 derived key. Verification recomputes the key and uses `hmac.compare_digest` to avoid ordinary byte-by-byte timing comparisons. The serialized record stores algorithm, work factor, salt, and digest; never store plaintext passwords.

Production systems should generally prefer a vetted Argon2id implementation when available, use rate limiting and MFA, and benchmark work factors for their hardware. PBKDF2 is used here because it is in the Python standard library. The iteration count is intentionally configurable to support future upgrades; `needs_rehash` flags older records. Do not log passwords or expose the demo's test password in a real system.
