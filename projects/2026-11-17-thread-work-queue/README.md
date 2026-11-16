# Bounded Concurrent Work Queue

Threaded bounded worker pool with ordered results, exception capture, graceful shutdown, and no third-party dependencies.

## Usage

Python 3.9+ and standard library only. Run `python tool.py` for the example/CLI; run `python -m unittest -v test_tool.py` from this directory for tests.

## Design, complexity, and limitations

Queue capacity limits pending jobs, not the accumulated output array. Results are returned in input order and failures are captured as Outcome.error. For blocking I/O tasks; CPU-bound Python work is constrained by the GIL.
