# Sparse Polynomial Arithmetic

Exact rational sparse polynomials with addition, multiplication, differentiation, evaluation, and zero-term normalization.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-12-polynomial-arithmetic
python polynomial.py
python -m unittest -v test_polynomial.py
```

## Design and limitations

The module is independently importable; the demonstration is guarded by `__main__`. Tests exercise normal and invalid inputs. This is an educational implementation, not a drop-in production service. Review resource limits, error handling, and threat models before deploying. See the module docstrings for the exact API and behavior.
