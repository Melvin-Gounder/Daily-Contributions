# IPv4 CIDR Policy Evaluator

First-match ordered CIDR rules with strict IPv4 validation and explainable decisions. O(R) per lookup for R rules. Pure simulation; does not change OS firewall settings.

## Run

Python 3.10+; no third-party dependencies.

    cd projects/2026-11-09-cidr-policy
    python policy.py
    python -m unittest -v test_policy.py

## Engineering notes

The implementation is self-contained and intended for learning and extension. Tests cover boundary conditions, invalid inputs, and core behavior. Read the source docstrings for API details.
