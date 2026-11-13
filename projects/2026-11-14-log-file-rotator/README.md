# Size-Based Log Rotation CLI

Rotating UTF-8 log writer with numbered backups, byte-based limits, and explicit oversize rejection.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-14-log-file-rotator
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Synchronous single-writer log rotation; no cross-process locking. UTF-8 byte sizes include newline.

## Testing

The included unittest suite exercises normal behavior, edge cases and invalid inputs. Run it locally before using the tool; automated execution was not available during publication.
