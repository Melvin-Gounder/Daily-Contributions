# RFC 6901 JSON Pointer Resolver

JSON Pointer path navigation with escape decoding, strict list indices, and error handling.

## Usage

Python 3.9+, standard library only. Run `python -m unittest -v test_tool.py` for tests. Run `python tool.py` for a demo.

## Design and limitations

Implements read-only JSON Pointer syntax, including ~0 and ~1 decoding. O(pointer length + traversal depth). Array indices disallow leading zeros. Not a JSON Patch implementation; paths are case-sensitive and no URI fragment decoding is performed.
