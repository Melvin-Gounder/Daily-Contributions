import unittest
from bloom import BloomFilter

class BloomTests(unittest.TestCase):
    def test_inserted_never_missing(self):
        b = BloomFilter(500)
        for i in range(500):
            b.add(str(i))
        self.assertTrue(all(b.contains(str(i)) for i in range(500)))
    def test_roundtrip(self):
        b = BloomFilter(10)
        b.add("abc")
        c = BloomFilter.from_json(b.to_json())
        self.assertTrue(c.contains("abc"))
        self.assertEqual(c.insertions, 1)
    def test_bytes(self):
        b = BloomFilter(10)
        b.add(b"binary")
        self.assertTrue(b.contains(b"binary"))
    def test_validation(self):
        with self.assertRaises(ValueError):
            BloomFilter(0)
        with self.assertRaises(ValueError):
            BloomFilter(5, 1)
        with self.assertRaises(TypeError):
            BloomFilter(5).add(123)
        with self.assertRaises(ValueError):
            BloomFilter.from_json('{"bits":2,"hashes":1,"insertions":0,"data":""}')
    def test_estimate(self):
        b = BloomFilter(20)
        self.assertEqual(b.estimated_false_positive_rate(), 0)
        b.add("x")
        self.assertGreater(b.estimated_false_positive_rate(), 0)

if __name__ == "__main__":
    unittest.main()
