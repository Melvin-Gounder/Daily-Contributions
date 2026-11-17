import unittest
from tool import optimize
class Tests(unittest.TestCase):
    def test_classic(self):
        cost,expression=optimize([30,35,15,5,10,20,25])
        self.assertEqual(cost,15125)
        self.assertEqual(expression.count("×"),5)
    def test_single(self): self.assertEqual(optimize([2,3]),(0,"A1"))
    def test_two(self): self.assertEqual(optimize([2,3,4]),(24,"(A1 × A2)"))
    def test_order_matters(self):
        self.assertEqual(optimize([10,100,5,50])[0],7500)
    def test_invalid(self):
        with self.assertRaises(ValueError): optimize([3,0,5])
        with self.assertRaises(ValueError): optimize([2])
    def test_ties(self):
        self.assertEqual(optimize([2,2,2,2])[0],16)
if __name__=="__main__": unittest.main()
