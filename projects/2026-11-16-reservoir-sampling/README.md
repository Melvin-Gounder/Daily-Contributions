# Streaming Reservoir Sampler

Uniform k-item sampling from an arbitrarily long stream with injected seeded RNG and reproducible CLI output.

## Requirements and usage

Python 3.9+; standard library only. From this directory:

```sh
python tool.py sample.jsonl -k 10 --seed 42
python -m unittest -v test_tool.py
```

## Design and complexity

Algorithm R replaces each held item with probability k/(i+1), so every seen item has equal inclusion probability. Seeded mode is for reproducibility, not cryptographic randomness.

## Scope

Educational reference implementation. Test with representative data and review resource limits before production use.
