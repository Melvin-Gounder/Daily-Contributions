"""Small strict JSON contract validator (not a full JSON Schema implementation)."""
import json

def validate(value, schema, path="$"):
    errors = []
    kind = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool,
             "integer": int, "number": (int, float), "null": type(None)}
    if kind not in types:
        raise ValueError("unsupported schema type")
    expected = types[kind]
    valid = isinstance(value, expected)
    if kind in ("integer", "number") and isinstance(value, bool):
        valid = False
    if not valid:
        return [f"{path}: expected {kind}"]
    if kind == "object":
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}.{key}: unexpected property")
        for key in props:
            if key in value:
                errors.extend(validate(value[key], props[key], f"{path}.{key}"))
    elif kind == "array":
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: too few items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: too many items")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate(item, schema["items"], f"{path}[{index}]"))
    elif kind in ("number", "integer"):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum")
    elif kind == "string":
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: too short")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: too long")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: not in enum")
    return errors

if __name__ == "__main__":
    contract = {"type": "object", "required": ["age"], "properties":
                {"age": {"type": "integer", "minimum": 0}}}
    print(json.dumps(validate({"age": -3}, contract), indent=2))
