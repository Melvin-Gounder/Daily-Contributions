"""Bloom filter: no false negatives for inserted values, possible false positives."""
import base64
import hashlib
import json
import math

class BloomFilter:
    def __init__(self, capacity, error_rate=0.01):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        if not 0 < error_rate < 1:
            raise ValueError("error_rate must be between zero and one")
        self.bits = max(1, math.ceil(-capacity * math.log(error_rate) / math.log(2)**2))
        self.hashes = max(1, round(self.bits / capacity * math.log(2)))
        self.data = bytearray((self.bits + 7) // 8)
        self.insertions = 0

    def _indices(self, value):
        if not isinstance(value, (bytes, str)):
            raise TypeError("values must be bytes or strings")
        raw = value.encode("utf-8") if isinstance(value, str) else value
        digest = hashlib.sha256(raw).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big") | 1
        for i in range(self.hashes):
            yield (h1 + i * h2) % self.bits

    def add(self, value):
        for index in self._indices(value):
            self.data[index // 8] |= 1 << (index % 8)
        self.insertions += 1

    def contains(self, value):
        return all(self.data[i // 8] & (1 << (i % 8)) for i in self._indices(value))

    def estimated_false_positive_rate(self):
        return (1 - math.exp(-self.hashes * self.insertions / self.bits)) ** self.hashes

    def to_json(self):
        return json.dumps({"bits":self.bits,"hashes":self.hashes,
                           "insertions":self.insertions,
                           "data":base64.b64encode(self.data).decode("ascii")})

    @classmethod
    def from_json(cls, raw):
        obj = json.loads(raw)
        bits, hashes, insertions = obj["bits"], obj["hashes"], obj["insertions"]
        if not all(type(x) is int and x > 0 for x in (bits, hashes)) or type(insertions) is not int or insertions < 0:
            raise ValueError("invalid metadata")
        if bits > 100_000_000 or hashes > 10000:
            raise ValueError("unreasonable filter size")
        data = base64.b64decode(obj["data"], validate=True)
        if len(data) != (bits + 7)//8:
            raise ValueError("invalid byte length")
        instance = cls(1)
        instance.bits, instance.hashes, instance.insertions = bits, hashes, insertions
        instance.data = bytearray(data)
        return instance

if __name__ == "__main__":
    b = BloomFilter(1000)
    for word in ("network", "database", "algorithm"):
        b.add(word)
    print(b.contains("network"), b.contains("missing"), b.estimated_false_positive_rate())
