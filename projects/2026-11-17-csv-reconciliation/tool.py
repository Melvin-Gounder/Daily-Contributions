"""Reconcile two keyed CSV snapshots with deterministic change reporting."""
import argparse
import csv
import json

def load(path, key):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if not fields or key not in fields or len(fields) != len(set(fields)):
            raise ValueError("invalid CSV header or missing key")
        records = {}
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("malformed CSV row")
            identifier = row[key]
            if not identifier or identifier in records:
                raise ValueError("empty or duplicate key")
            records[identifier] = row
        return fields, records

def reconcile(before_path, after_path, key):
    before_fields, before = load(before_path, key)
    after_fields, after = load(after_path, key)
    if set(before_fields) != set(after_fields):
        raise ValueError("schema drift between snapshots")
    added = {k: after[k] for k in sorted(after.keys() - before.keys())}
    removed = {k: before[k] for k in sorted(before.keys() - after.keys())}
    modified = {}
    for k in sorted(before.keys() & after.keys()):
        changes = {field: {"old": before[k][field], "new": after[k][field]}
                   for field in sorted(before_fields) if before[k][field] != after[k][field]}
        if changes:
            modified[k] = changes
    return {"added": added, "removed": removed, "modified": modified}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("before")
    p.add_argument("after")
    p.add_argument("--key", required=True)
    a = p.parse_args()
    print(json.dumps(reconcile(a.before, a.after, a.key), indent=2))
