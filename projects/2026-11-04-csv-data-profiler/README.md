# Streaming CSV Data Quality Profiler

Run `python profile_csv.py example.csv` for a JSON report, or `python -m unittest -v test_profile_csv.py` for tests.

The tool reads rows incrementally with `csv.DictReader`, checks unique nonempty headers, counts blank cells and malformed rows, and computes per-column finite numeric minimum, maximum, and mean with `Decimal`. It works without third-party libraries and uses memory proportional to the number of columns rather than the number of rows. Non-numeric cells are ignored for numeric summaries, not treated as zero. Malformed rows count toward total rows but are excluded from column statistics. This is a data-quality overview, not a schema inference or CSV security sanitizer; do not blindly open untrusted CSV cells in spreadsheet programs.
