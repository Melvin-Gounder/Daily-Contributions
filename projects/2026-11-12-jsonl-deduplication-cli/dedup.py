import argparse
import json
import os
import tempfile
from pathlib import Path

def extract(obj, dotted):
    value = obj
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"missing key {dotted!r}")
        value = value[part]
    if isinstance(value,(dict,list)):
        raise ValueError("dedup key must be scalar")
    return json.dumps(value, sort_keys=True, ensure_ascii=False)

def deduplicate(source, destination, key):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("source and destination must differ")
    if not key or any(not part for part in key.split(".")):
        raise ValueError("invalid dotted key")
    seen, kept, dropped = set(), 0, 0
    temp_path = None
    try:
        with source.open("r",encoding="utf-8") as reader:
            with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=destination.parent,delete=False) as writer:
                temp_path = Path(writer.name)
                for number,line in enumerate(reader,1):
                    try:
                        obj = json.loads(line)
                        identity = extract(obj,key)
                    except (ValueError,TypeError) as exc:
                        raise ValueError(f"line {number}: {exc}") from exc
                    if identity in seen:
                        dropped += 1
                    else:
                        seen.add(identity)
                        writer.write(json.dumps(obj,ensure_ascii=False,separators=(",",":"))+"\n")
                        kept += 1
        os.replace(temp_path,destination)
        return kept,dropped
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Keep first record for each JSONL key")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--key",required=True,help="Dotted path, e.g. user.id")
    args=parser.parse_args()
    print("kept, duplicates:", *deduplicate(args.source,args.destination,args.key))
