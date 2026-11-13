import unittest
from tool import IntervalSet

class Tests(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(IntervalSet([(5,8),(1,3),(3,5)]).ranges,((1,8),))
    def test_set_operations(self):
        a=IntervalSet([(1,10)]); b=IntervalSet([(3,5),(7,12)])
        self.assertEqual(a.intersection(b).ranges,((3,5),(7,10)))
        self.assertEqual(a.difference(b).ranges,((1,3),(5,7)))
        self.assertEqual(a.union(b).ranges,((1,12),))
    def test_membership_and_validation(self):
        a=IntervalSet([(2,4)])
        self.assertTrue(2 in a); self.assertFalse(4 in a)
        with self.assertRaises(ValueError): IntervalSet([(3,3)])
if __name__=="__main__": unittest.main()
