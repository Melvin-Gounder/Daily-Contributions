"""Merge sorted integer files with bounded memory."""
import argparse
import heapq
import os
import tempfile
from pathlib import Path

def read_sorted(path):
    previous=None
    with open(path,encoding="utf-8") as stream:
        for line_no,line in enumerate(stream,1):
            if not line.strip(): continue
            try: value=int(line.strip())
            except ValueError as exc: raise ValueError(f"{path}:{line_no}: invalid integer") from exc
            if previous is not None and value<previous:
                raise ValueError(f"{path}:{line_no}: input not sorted")
            previous=value
            yield value

def merge(paths):
    yield from heapq.merge(*(read_sorted(p) for p in paths))

def merge_to_file(paths, destination):
    dest=Path(destination)
    if any(dest.resolve()==Path(p).resolve() for p in paths):
        raise ValueError("output cannot overwrite an input")
    fd,name=tempfile.mkstemp(prefix=".merge-",dir=dest.parent,text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as output:
            for number in merge(paths): output.write(f"{number}\n")
            output.flush(); os.fsync(output.fileno())
        os.replace(name,dest)
    finally:
        if os.path.exists(name): os.unlink(name)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("inputs",nargs="+")
    args=parser.parse_args()
    merge_to_file(args.inputs,args.output)
