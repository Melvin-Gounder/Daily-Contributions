"""Deterministic Bloom filter; false positives possible, false negatives not expected."""
import base64
import hashlib
import json
import math

class BloomFilter:
    def __init__(self, capacity, error_rate=0.01, *, bits=None, hashes=None):
        if not isinstance(capacity, int) or capacity <= 0 or not 0 < error_rate < 1:
            raise ValueError("invalid capacity or error rate")
        self.capacity = capacity
        self.error_rate = error_rate
        self.m = bits or max(1, math.ceil(-capacity * math.log(error_rate) / math.log(2)**2))
        self.k = hashes or max(1, round(self.m / capacity * math.log(2)))
        if self.m <= 0 or self.k <= 0:
            raise ValueError("invalid filter dimensions")
        self.data = bytearray((self.m + 7) // 8)
        self.insertions = 0

    def _indices(self, value):
        if not isinstance(value, str):
            raise TypeError("items must be strings")
        digest = hashlib.sha256(value.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big") | 1
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, value):
        for index in self._indices(value):
            self.data[index // 8] |= 1 << (index % 8)
        self.insertions += 1

    def __contains__(self, value):
        return all(self.data[index // 8] & (1 << (index % 8)) for index in self._indices(value))

    def estimated_false_positive_rate(self):
        return (1 - math.exp(-self.k * self.insertions / self.m)) ** self.k

    def dump(self):
        return json.dumps({"capacity": self.capacity, "error_rate": self.error_rate,
                           "m": self.m, "k": self.k, "insertions": self.insertions,
                           "data": base64.b64encode(self.data).decode("ascii")})

    @classmethod
    def load(cls, payload):
        obj = json.loads(payload)
        result = cls(obj["capacity"], obj["error_rate"], bits=obj["m"], hashes=obj["k"])
        data = base64.b64decode(obj["data"], validate=True)
        if len(data) != len(result.data) or not isinstance(obj["insertions"], int) or obj["insertions"] < 0:
            raise ValueError("invalid serialized filter")
        result.data[:] = data
        result.insertions = obj["insertions"]
        return result

if __name__ == "__main__":
    f = BloomFilter(1000)
    for word in ("alpha", "beta", "gamma"):
        f.add(word)
    print({word: word in f for word in ("alpha", "delta")})
