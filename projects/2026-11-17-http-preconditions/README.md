# HTTP Conditional Request Evaluator

RFC-inspired If-Match, If-None-Match and method-dependent 304/412 decisions with strong versus weak ETag comparison.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

A teaching subset of RFC 9110 entity-tag preconditions; does not implement date validators, Range, or full HTTP field parsing. ETags are opaque quoted strings.
