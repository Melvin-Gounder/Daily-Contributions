# Length-Prefixed TCP Frame Decoder

Incremental binary protocol framing with maximum-size enforcement, fragmented packet handling, and EOF truncation checks.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

Frames have a 4-byte unsigned network-order length. Decoder buffers at most one incomplete frame plus newly received input; callers should bound feed chunk sizes. Does not implement sockets or authentication.
