# DNS Zone Record Linter

Offline DNS record validation for A, AAAA, CNAME, MX and TXT, including conflicting CNAME detection.

## Usage

Python 3.9+; Python standard library only.

```sh
cd projects/2026-11-15-dns-zone-linter
python tool.py
python -m unittest -v test_tool.py
```

## Design

Offline DNS record validation for A, AAAA, CNAME, MX and TXT, including conflicting CNAME detection. Designed as an educational, dependency-free implementation with deterministic unit tests and explicit input checks.

## Limitations

Small-scale demonstration, not a production service. Review concurrency, security, performance, and input limits before deployment.
