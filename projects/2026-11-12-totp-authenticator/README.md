# Time-Based One-Time Password Authenticator

RFC 6238-compatible HMAC-SHA1 TOTP generation and bounded-window verification with constant-time comparisons and published test vectors.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-12-totp-authenticator
python totp.py
python -m unittest -v test_totp.py
```

## Design and limitations

The module is independently importable; the demonstration is guarded by `__main__`. Tests exercise normal and invalid inputs. This is an educational implementation, not a drop-in production service. Review resource limits, error handling, and threat models before deploying. See the module docstrings for the exact API and behavior.
