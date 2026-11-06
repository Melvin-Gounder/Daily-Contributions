"""Small declarative JSON validator; not a full JSON Schema implementation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Problem:
    path: str
    message: str

def validate(value, spec, path="$"):
    """Return all validation problems; spec supports type, required, properties, items, min, max."""
    problems = []
    kind = spec.get("type")
    types = {"object":lambda x:isinstance(x,dict),
             "array":lambda x:isinstance(x,list),
             "string":lambda x:isinstance(x,str),
             "integer":lambda x:type(x) is int,
             "number":lambda x:type(x) in (int,float),
             "boolean":lambda x:type(x) is bool,
             "null":lambda x:x is None}
    if kind not in types:
        raise ValueError("unsupported schema type: " + repr(kind))
    if not types[kind](value):
        return [Problem(path, "expected " + kind)]
    if kind == "object":
        props = spec.get("properties", {})
        for name in spec.get("required", []):
            if name not in value:
                problems.append(Problem(path + "." + name, "required"))
        if spec.get("additional", True) is False:
            for name in value:
                if name not in props:
                    problems.append(Problem(path + "." + str(name), "unexpected field"))
        for name, child in props.items():
            if name in value:
                problems.extend(validate(value[name], child, path + "." + name))
    elif kind == "array":
        if "min" in spec and len(value) < spec["min"]:
            problems.append(Problem(path, "too few items"))
        if "max" in spec and len(value) > spec["max"]:
            problems.append(Problem(path, "too many items"))
        if "items" in spec:
            for i, item in enumerate(value):
                problems.extend(validate(item, spec["items"], f"{path}[{i}]"))
    elif kind == "string":
        if "min" in spec and len(value) < spec["min"]:
            problems.append(Problem(path, "too short"))
        if "max" in spec and len(value) > spec["max"]:
            problems.append(Problem(path, "too long"))
    elif kind in ("number", "integer"):
        if "min" in spec and value < spec["min"]:
            problems.append(Problem(path, "below minimum"))
        if "max" in spec and value > spec["max"]:
            problems.append(Problem(path, "above maximum"))
    return problems

if __name__ == "__main__":
    contract = {"type":"object","required":["name","scores"],"additional":False,
                "properties":{"name":{"type":"string","min":1},
                              "scores":{"type":"array","items":{"type":"integer","min":0,"max":100}}}}
    print(validate({"name":"Ada","scores":[98,105]},contract))
