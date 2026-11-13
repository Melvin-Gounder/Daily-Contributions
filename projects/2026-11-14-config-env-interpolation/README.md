# Safe Environment Configuration Resolver

Recursive environment-variable interpolation with defaults, cycle detection, and explicit missing-variable errors.

## Run

Python 3.9+; standard library only.

```sh
cd projects/2026-11-14-config-env-interpolation
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

No shell expansion or command execution. Defaults apply to missing or empty values; recursive cycles are rejected.

The included tests cover representative and error cases; execute them locally before deployment.
