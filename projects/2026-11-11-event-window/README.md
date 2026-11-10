# Out-of-Order Event Window Aggregator

Event-time tumbling windows, watermarks, late-event rejection, and deterministic aggregation.

## Usage

Requires Python 3.10+ and only the standard library.

```bash
cd projects/2026-11-11-event-window
python windows.py
python -m unittest -v test_windows.py
```

## Design

The module provides a reusable API; see the demo and isolated tests for examples and boundary conditions. Late data is rejected based on event time; windows are emitted only when the watermark reaches their end.
