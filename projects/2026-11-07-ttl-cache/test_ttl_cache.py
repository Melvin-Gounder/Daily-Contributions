import unittest
from ttl_cache import TTLCache

class Clock:
    now = 0
    def __call__(self):
        return self.now

class TTLTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.cache = TTLCache(2, 5, clock=self.clock)
    def test_expiry_boundary(self):
        self.cache.put("a", 1)
        self.clock.now = 4.99
        self.assertEqual(self.cache.get("a"), 1)
        self.clock.now = 5
        self.assertIsNone(self.cache.get("a"))
    def test_lru_eviction(self):
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.get("a")
        self.cache.put("c", 3)
        self.assertIsNone(self.cache.get("b"))
        self.assertEqual(self.cache.get("a"), 1)
    def test_refresh(self):
        self.cache.put("a", 1)
        self.clock.now = 4
        self.cache.put("a", 2)
        self.clock.now = 6
        self.assertEqual(self.cache.get("a"), 2)
    def test_delete(self):
        self.cache.put("a", 1)
        self.assertTrue(self.cache.delete("a"))
        self.assertFalse(self.cache.delete("a"))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            TTLCache(0, 1)
        with self.assertRaises(ValueError):
            TTLCache(1, 0)

if __name__ == "__main__":
    unittest.main()
