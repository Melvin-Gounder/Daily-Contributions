# Unicode-Aware Text Token Index

Inverted positional index with phrase search, Boolean AND queries, document replacement, and deterministic results.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

Casefolds Unicode and tokenizes word runs, ignoring underscores and punctuation. Positional phrase queries require contiguous tokens. Designed for small in-memory corpora, not large-scale ranking.
