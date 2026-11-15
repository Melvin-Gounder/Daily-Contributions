"""Small MVCC model: snapshots read the latest version <= their revision."""
from bisect import bisect_right

class Store:
    def __init__(self):
        self.revision = 0
        self.history = {}

    def put(self, key, value):
        self.revision += 1
        self.history.setdefault(key, []).append((self.revision, False, value))
        return self.revision

    def delete(self, key):
        self.revision += 1
        self.history.setdefault(key, []).append((self.revision, True, None))
        return self.revision

    def snapshot(self):
        return self.revision

    def get(self, key, revision=None, default=None):
        revision = self.revision if revision is None else revision
        if not isinstance(revision, int) or not 0 <= revision <= self.revision:
            raise ValueError("invalid snapshot revision")
        versions = self.history.get(key, [])
        index = bisect_right(versions, revision, key=lambda entry: entry[0]) - 1
        if index < 0 or versions[index][1]:
            return default
        return versions[index][2]

    def scan(self, revision=None):
        return {key: self.get(key, revision) for key in sorted(self.history)
                if self._exists(key, revision)}

    def _exists(self, key, revision):
        marker = object()
        return self.get(key, revision, marker) is not marker

if __name__ == "__main__":
    s = Store()
    s.put("feature", "v1")
    old = s.snapshot()
    s.put("feature", "v2")
    print(s.get("feature", old), s.get("feature"))
