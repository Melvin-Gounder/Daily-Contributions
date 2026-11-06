# Recursive JSON Contract Validator

A small, dependency-free validator for API request bodies and configuration payloads. It reports **all** problems with precise nested paths instead of failing on the first issue.

## Run
```sh
cd projects/2026-11-07-json-schema-lite
python validator.py
python -m unittest -v
```

A schema is a dictionary with `type` and optional `required`, `properties`, `additional`, `items`, `min`, and `max`. Supports objects, arrays, strings, integers, numbers, booleans, and nulls. Python booleans are intentionally excluded from integer/number types.

## Design
Recursive descent traverses each schema-covered value once, O(n) for n visited fields/items (ignoring dictionary lookup overhead). Error storage is O(e), recursion depth O(d). This is **not** the JSON Schema standard: it omits references, unions, formats, patterns, and more. Never use it as a replacement for production-grade validation of untrusted schemas; callers should supply trusted schema definitions and enforce payload size/depth limits.
