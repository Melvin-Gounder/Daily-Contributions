"""Welford's online variance and parallel mergeable summary."""
import argparse
import math
from dataclasses import dataclass

@dataclass
class Stats:
    count: int = 0
    mean: float = 0.0
    m2: float = 0.0

    def add(self, value):
        x = float(value)
        if not math.isfinite(x):
            raise ValueError("input must be finite")
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        self.m2 += delta * (x - self.mean)
        return self

    def merge(self, other):
        if not other.count:
            return self
        if not self.count:
            self.count, self.mean, self.m2 = other.count, other.mean, other.m2
            return self
        n = self.count + other.count
        delta = other.mean - self.mean
        self.m2 += other.m2 + delta * delta * self.count * other.count / n
        self.mean += delta * other.count / n
        self.count = n
        return self

    def variance(self, sample=True):
        minimum = 2 if sample else 1
        if self.count < minimum:
            raise ValueError("insufficient observations")
        return max(0.0, self.m2 / (self.count - (1 if sample else 0)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("values", nargs="+", type=float)
    args = parser.parse_args()
    s = Stats()
    for x in args.values:
        s.add(x)
    print(f"n={s.count}, mean={s.mean:g}, population_variance={s.variance(False):g}")
if __name__ == "__main__":
    main()
