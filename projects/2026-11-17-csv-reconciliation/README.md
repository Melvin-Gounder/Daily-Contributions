# Dependency-Free CSV Reconciliation

Compare keyed CSV snapshots to report inserted, removed, and modified rows, rejecting duplicate keys and schema drift.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

Uses a hash map keyed by a designated unique column; O(n+m) average comparisons and O(n+m) memory. Compares string field values exactly; does not coerce numbers or dates.
