# Typed Environment Configuration

Run `python config.py` for a demo; `APP_PORT=9000 DEBUG=true python config.py` overrides defaults. Run `python -m unittest -v test_config.py`.

Declare expected fields with `Field(parser, required, default, minimum, maximum, secret)`. `validate(schema, mapping)` converts strings into typed values, checks numeric bounds, aggregates errors, and never includes raw values in validation errors. Missing optional values receive explicit defaults. Unknown input keys are ignored, allowing an entire process environment to be passed safely. Do not print returned dictionaries containing secrets in production; the demo intentionally contains no secret fields. The parser callback must be trusted application code.
