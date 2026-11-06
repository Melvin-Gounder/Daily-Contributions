"""Bounded TTL cache using monotonic time and OrderedDict."""
from collections import OrderedDict
import time

class TTLCache:
    def __init__(self, capacity, ttl_seconds, clock=time.monotonic):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("capacity must be positive")
        if ttl_seconds <= 0:
            raise ValueError("TTL must be positive")
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.clock = clock
        self.items = OrderedDict()

    def _purge(self):
        now = self.clock()
        for key in list(self.items):
            if self.items[key][1] <= now:
                del self.items[key]

    def put(self, key, value):
        self._purge()
        self.items.pop(key, None)
        self.items[key] = (value, self.clock() + self.ttl)
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)

    def get(self, key, default=None):
        self._purge()
        if key not in self.items:
            return default
        self.items.move_to_end(key)
        return self.items[key][0]

    def delete(self, key):
        self._purge()
        return self.items.pop(key, None) is not None

    def __len__(self):
        self._purge()
        return len(self.items)

if __name__ == "__main__":
    cache = TTLCache(2, 30)
    cache.put("user:1", {"name":"Ada"})
    print(cache.get("user:1"))
