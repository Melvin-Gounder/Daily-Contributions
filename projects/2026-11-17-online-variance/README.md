# Streaming Online Variance Calculator

Numerically stable Welford variance, parallel-statistics merging, sample/population estimates, and CLI input validation.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

One-pass O(n) time and O(1) space; merge enables distributed map/reduce. Floating-point rounding remains possible for extreme magnitudes.
