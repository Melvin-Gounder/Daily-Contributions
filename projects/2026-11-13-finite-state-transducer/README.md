# Finite-State Text Normalizer

Composable streaming character transformations with whitespace collapse and stateful punctuation handling.

## Run

Requires Python 3.9+ (standard library only).

```sh
cd projects/2026-11-13-finite-state-transducer
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

O(n) time, O(1) state excluding returned output. Streaming chunks preserve whitespace state; punctuation-adjacent spaces are removed.

The public functions in `tool.py` can be imported into another program. Tests cover examples, edge cases and invalid inputs. This is a learning implementation; assess operational constraints before production use.
