import unittest
from fractions import Fraction
from tool import quantile,median
class Tests(unittest.TestCase):
    def test_weighted(self):
        data=[(1,1),(10,3),(100,1)]
        self.assertEqual(median(data),10);self.assertEqual(quantile(data,1),100)
    def test_exact(self):
        self.assertEqual(quantile([("0.1","0.2"),("0.3","0.8")],Fraction(1,5)),Fraction(1,10))
    def test_duplicate(self):
        self.assertEqual(median([(2,1),(2,2),(3,1)]),2)
    def test_reject(self):
        for data in [[],[(1,0)],[(1,-2)]]:
            with self.assertRaises(ValueError): median(data)
        with self.assertRaises(ValueError): quantile([(1,1)],2)
if __name__=="__main__": unittest.main()
