# Five-Field Cron Expression Planner

Cron field parser with ranges, lists, steps, weekday semantics, and bounded minute-by-minute schedule search.

## Run

Requires Python 3.9+ and only the standard library.

```sh
cd projects/2026-11-12-cron-expression-planner
python cron.py
python -m unittest -v test_cron.py
```

## Design and limitations

The module is independently importable; the demonstration is guarded by `__main__`. Tests exercise normal and invalid inputs. This is an educational implementation, not a drop-in production service. Review resource limits, error handling, and threat models before deploying. See the module docstrings for the exact API and behavior.
