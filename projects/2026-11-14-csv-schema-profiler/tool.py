import csv
import json
import math
from collections import Counter

def profile(path, sample_limit=12):
    if not isinstance(sample_limit,int) or sample_limit<0: raise ValueError("invalid sample_limit")
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames):
            raise ValueError("missing or duplicate headers")
        columns={k:{"nonempty":0,"missing":0,"numeric":0,"min":None,"max":None,"examples":[]} for k in reader.fieldnames}
        rows=0
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("ragged CSV row")
            rows+=1
            for key,raw in row.items():
                col=columns[key]
                value=raw.strip()
                if not value:
                    col["missing"]+=1
                    continue
                col["nonempty"]+=1
                if value not in col["examples"] and len(col["examples"])<sample_limit:
                    col["examples"].append(value)
                try:
                    num=float(value)
                    if not math.isfinite(num): continue
                except ValueError: continue
                col["numeric"]+=1
                col["min"]=num if col["min"] is None else min(num,col["min"])
                col["max"]=num if col["max"] is None else max(num,col["max"])
    for col in columns.values():
        col["inferred_type"]="number" if col["nonempty"] and col["numeric"]==col["nonempty"] else "text"
    return {"rows":rows,"columns":columns}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("csv_path"); args=p.parse_args()
    print(json.dumps(profile(args.csv_path),indent=2))
