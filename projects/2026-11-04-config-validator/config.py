"""Small declarative configuration validator without dependencies."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Field:
    parser: Callable
    required: bool = True
    default: object = None
    minimum: object = None
    maximum: object = None
    secret: bool = False

def boolean(value):
    normalized = value.strip().lower()
    if normalized in ("true", "1", "yes", "on"): return True
    if normalized in ("false", "0", "no", "off"): return False
    raise ValueError("expected boolean")

def validate(schema, values):
    errors, result = [], {}
    for key, spec in schema.items():
        raw = values.get(key)
        if raw is None or raw == "":
            if spec.required:
                errors.append(f"{key}: missing required value")
                continue
            result[key] = spec.default
            continue
        try:
            parsed = spec.parser(raw)
            if spec.minimum is not None and parsed < spec.minimum:
                raise ValueError("below minimum")
            if spec.maximum is not None and parsed > spec.maximum:
                raise ValueError("above maximum")
            result[key] = parsed
        except (ValueError, TypeError, OverflowError):
            errors.append(f"{key}: invalid value" + (" (redacted)" if spec.secret else ""))
    if errors:
        raise ValueError("; ".join(errors))
    return result

if __name__ == "__main__":
    import os
    schema = {"APP_PORT": Field(int, minimum=1, maximum=65535),
              "DEBUG": Field(boolean, required=False, default=False),
              "WORKERS": Field(int, required=False, default=4, minimum=1, maximum=64)}
    print(validate(schema, {"APP_PORT": os.environ.get("APP_PORT", "8080"),
                            "DEBUG": os.environ.get("DEBUG"),
                            "WORKERS": os.environ.get("WORKERS")}))
