import random
import unittest
from tool import sample

class Tests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(sample(range(100), 0), [])
    def test_short_stream(self):
        self.assertEqual(sample(iter([1, 2]), 5), [1, 2])
    def test_reproducible(self):
        self.assertEqual(sample(range(100), 8, random.Random(42)), sample(range(100), 8, random.Random(42)))
    def test_unique(self):
        self.assertEqual(len(set(sample(range(1000), 40, random.Random(1)))), 40)
    def test_bad_k(self):
        for k in (-1, True, 1.5):
            with self.assertRaises(ValueError): sample([], k)
if __name__ == "__main__": unittest.main()
