# Sorted Calendar Conflict Index

Ordered half-open bookings with overlap checks, cancellation, and minimum-duration free-slot discovery.

Run: `python tool.py`. Tests: `python -m unittest -v test_tool.py`. Python 3.9+, standard library only.

## Design

Bookings are sorted by start time and modeled as half-open intervals, so adjacent bookings do not overlap. Binary search finds the insertion point in O(log n), while list insertion is O(n). Free-slot scans are O(n), storage O(n). Names are unique. Time units are caller-defined integers; this is not a timezone-aware scheduling system.
