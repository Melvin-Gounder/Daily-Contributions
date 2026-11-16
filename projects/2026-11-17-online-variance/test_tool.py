import unittest
from tool import Stats
class Tests(unittest.TestCase):
    def test_known_values(self):
        s = Stats()
        for x in [2, 4, 4, 4, 5, 5, 7, 9]: s.add(x)
        self.assertAlmostEqual(s.mean, 5)
        self.assertAlmostEqual(s.variance(False), 4)
    def test_merge(self):
        a, b = Stats(), Stats()
        for x in [1, 2]: a.add(x)
        for x in [3, 4]: b.add(x)
        a.merge(b)
        self.assertAlmostEqual(a.variance(False), 1.25)
    def test_edge(self):
        with self.assertRaises(ValueError): Stats().variance()
        with self.assertRaises(ValueError): Stats().add(float("nan"))
if __name__ == "__main__": unittest.main()
