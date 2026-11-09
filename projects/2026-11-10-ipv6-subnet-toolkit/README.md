# IPv6 Subnet Toolkit

Strict IPv6 network parsing, address containment, subnet partitioning, and deterministic host-address allocation with prefix bounds.

## Run

Requires Python 3.10+ and only the standard library. From this project directory:

```bash
python toolkit.py
python -m unittest -v test_toolkit.py
```

## Design and limitations

The implementation requires canonical network boundaries (strict mode), not host CIDRs. IPv6 has no broadcast traffic; the 'last' field denotes the final address, not a broadcast endpoint. Splits are bounded to avoid accidental exponential allocation.

## Learning objectives

Read the implementation and tests together to understand invariants, input validation, boundary cases, and failure behavior. Extend the tests before modifying core logic.
