# Recursive JSON Contract Validator

Dependency-free validation of nested JSON objects, arrays, required keys, numeric bounds, and path-specific errors.

## Usage and design

Run `python tool.py` and `python -m unittest -v test_tool.py`. Supports a deliberately documented subset of JSON Schema-like constraints: type, object properties/required/additionalProperties, array items/size, string length, numeric bounds and enum. Reports all discoverable errors with JSON-style paths. Complexity O(number of visited nodes); no external dependencies. Schemas should be trusted; this is not an official JSON Schema validator.
