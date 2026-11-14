"""JSON Merge Patch per RFC 7396 (not JSON Patch RFC 6902)."""
import copy
import json

def merge_patch(target, patch):
    """Return a new value; null in object patch deletes the property."""
    if not isinstance(patch, dict):
        return copy.deepcopy(patch)
    if not isinstance(target, dict):
        target = {}
    result = copy.deepcopy(target)
    for key, value in patch.items():
        if not isinstance(key, str):
            raise TypeError("JSON object keys must be strings")
        if value is None:
            result.pop(key,None)
        else:
            result[key] = merge_patch(result.get(key),value)
    return result

def apply_json(target_text, patch_text):
    target = json.loads(target_text)
    patch = json.loads(patch_text)
    return json.dumps(merge_patch(target,patch),sort_keys=True,separators=(",",":"))

if __name__ == "__main__":
    print(apply_json('{"title":"Goodbye!","author":{"name":"John"},"tags":["example"]}', '{"title":"Hello!","author":{"name":null},"tags":["new"]}'))
