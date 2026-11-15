import unittest
from tool import SegmentTree
class Tests(unittest.TestCase):
    def test_updates(self):
        s = SegmentTree([1, 2, 3, 4])
        s.add(1, 4, 5)
        self.assertEqual(s.sum(0, 4), 25)
        self.assertEqual(s.sum(1, 3), 15)
        s.add(0, 2, -2)
        self.assertEqual(s.sum(0, 4), 21)
        self.assertEqual(s.sum(0, 1), -1)
    def test_empty(self):
        s = SegmentTree([])
        self.assertEqual(s.sum(0, 0), 0)
        with self.assertRaises(IndexError): s.add(0, 1, 3)
    def test_naive(self):
        a = list(range(30))
        s = SegmentTree(a)
        for left, right, delta in [(0,30,3),(4,18,-2),(12,13,10),(0,1,-4)]:
            s.add(left,right,delta)
            a[left:right] = [x+delta for x in a[left:right]]
        for i in range(31):
            for j in range(i,31):
                self.assertEqual(s.sum(i,j), sum(a[i:j]))
if __name__ == "__main__": unittest.main()
