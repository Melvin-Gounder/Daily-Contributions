# HMAC CSV Pseudonymization CLI

Streaming CSV pseudonyms using keyed SHA-256, stable joins and configurable protected columns.

## Usage

Python 3.9+; Python standard library only.

```sh
cd projects/2026-11-15-csv-pseudonymizer
python tool.py
python -m unittest -v test_tool.py
```

## Design

Streaming CSV pseudonyms using keyed SHA-256, stable joins and configurable protected columns. Designed as an educational, dependency-free implementation with deterministic unit tests and explicit input checks.

## Limitations

Small-scale demonstration, not a production service. Review concurrency, security, performance, and input limits before deployment.
