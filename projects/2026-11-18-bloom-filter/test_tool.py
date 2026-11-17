import unittest
from tool import BloomFilter

class Tests(unittest.TestCase):
    def test_present(self):
        f = BloomFilter(20)
        for item in ("a","b","c"):
            f.add(item)
        self.assertTrue(all(item in f for item in ("a","b","c")))
    def test_roundtrip(self):
        f = BloomFilter(10)
        f.add("hello")
        restored = BloomFilter.load(f.dump())
        self.assertIn("hello", restored)
        self.assertEqual(restored.dump(), f.dump())
    def test_rate(self):
        f = BloomFilter(100)
        self.assertEqual(f.estimated_false_positive_rate(), 0)
        f.add("x")
        self.assertGreater(f.estimated_false_positive_rate(), 0)
    def test_bad_capacity(self):
        with self.assertRaises(ValueError):
            BloomFilter(0)
    def test_non_string(self):
        with self.assertRaises(TypeError):
            BloomFilter(10).add(123)

if __name__ == "__main__":
    unittest.main()
