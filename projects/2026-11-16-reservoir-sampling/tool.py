"""Uniform reservoir sampling (Algorithm R), O(n) time and O(k) memory."""
import argparse
import json
import random

def sample(iterable, k, rng=None):
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    rng = rng if rng is not None else random.SystemRandom()
    reservoir = []
    for i, item in enumerate(iterable):
        if i < k:
            reservoir.append(item)
        else:
            j = rng.randrange(i + 1)
            if j < k:
                reservoir[j] = item
    return reservoir

def main():
    parser = argparse.ArgumentParser(description="Sample JSONL records without loading the whole file")
    parser.add_argument("path")
    parser.add_argument("-k", type=int, required=True)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    with open(args.path, encoding="utf-8") as stream:
        records = (json.loads(line) for line in stream if line.strip())
        for record in sample(records, args.k, rng):
            print(json.dumps(record, ensure_ascii=False))
if __name__ == "__main__":
    main()
