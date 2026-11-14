import unittest
from tool import Fenwick

class Tests(unittest.TestCase):
    def test_ranges(self):
        f = Fenwick([1,2,3,4])
        self.assertEqual(f.prefix(0),0)
        self.assertEqual(f.range_sum(1,3),5)
        self.assertEqual(f.prefix(4),10)
    def test_updates(self):
        f = Fenwick([1,2,3])
        f.add(0,4); f.set(2,-2)
        self.assertEqual(f.range_sum(0,3),5)
    def test_empty_and_invalid(self):
        self.assertEqual(Fenwick([]).prefix(0),0)
        with self.assertRaises(IndexError): Fenwick([1]).range_sum(0,2)
if __name__ == "__main__": unittest.main()
