"""Streaming CSV data quality report; standard library only."""
import argparse
import csv
import json
from collections import Counter
from decimal import Decimal, InvalidOperation

def profile(path):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        if not columns or len(set(columns)) != len(columns) or any(not c for c in columns):
            raise ValueError("CSV needs unique nonempty headers")
        rows, malformed = 0, 0
        missing = Counter({c:0 for c in columns})
        numeric = {c: {"count":0,"sum":Decimal(0),"min":None,"max":None} for c in columns}
        for row in reader:
            rows += 1
            if None in row or any(value is None for value in row.values()):
                malformed += 1
                continue
            for col in columns:
                value = row[col].strip()
                if not value:
                    missing[col] += 1
                    continue
                try:
                    number = Decimal(value)
                    if not number.is_finite(): continue
                except InvalidOperation:
                    continue
                stats = numeric[col]
                stats["count"] += 1
                stats["sum"] += number
                stats["min"] = number if stats["min"] is None else min(stats["min"], number)
                stats["max"] = number if stats["max"] is None else max(stats["max"], number)
    return {"rows":rows,"malformed_rows":malformed,"columns":{
        col: {"missing":missing[col], "numeric_count":numeric[col]["count"],
              "numeric_min":str(numeric[col]["min"]) if numeric[col]["min"] is not None else None,
              "numeric_max":str(numeric[col]["max"]) if numeric[col]["max"] is not None else None,
              "numeric_mean":str(numeric[col]["sum"]/numeric[col]["count"]) if numeric[col]["count"] else None}
        for col in columns}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile a CSV file")
    parser.add_argument("file")
    args = parser.parse_args()
    try: print(json.dumps(profile(args.file), indent=2))
    except (OSError, ValueError, csv.Error) as exc: parser.error(str(exc))
