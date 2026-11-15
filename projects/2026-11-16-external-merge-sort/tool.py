"""External integer sort with temporary sorted runs and heap merge."""
import argparse
import heapq
import os
import tempfile
from contextlib import ExitStack

def sort_file(source, destination, chunk_size=10000):
    if chunk_size < 1: raise ValueError("chunk_size must be positive")
    if os.path.abspath(source) == os.path.abspath(destination):
        raise ValueError("source and destination must differ")
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        with open(source, encoding="utf-8") as stream:
            while True:
                chunk = []
                for _ in range(chunk_size):
                    line = stream.readline()
                    if not line: break
                    chunk.append(int(line.strip()))
                if not chunk: break
                chunk.sort()
                path = os.path.join(temp, str(len(paths)) + ".txt")
                with open(path, "w", encoding="utf-8") as out:
                    out.writelines(str(value) + "\n" for value in chunk)
                paths.append(path)
        directory = os.path.dirname(os.path.abspath(destination))
        fd, staging = tempfile.mkstemp(dir=directory, prefix=".sort-", text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as out, ExitStack() as stack:
                streams = [stack.enter_context(open(path, encoding="utf-8")) for path in paths]
                merged = heapq.merge(*(map(int, stream) for stream in streams))
                for value in merged: out.write(str(value) + "\n")
            os.replace(staging, destination)
        finally:
            if os.path.exists(staging): os.unlink(staging)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("destination")
    p.add_argument("--chunk-size", type=int, default=10000)
    a = p.parse_args()
    sort_file(a.source, a.destination, a.chunk_size)
