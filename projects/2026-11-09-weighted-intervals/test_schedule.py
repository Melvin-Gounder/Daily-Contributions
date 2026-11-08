from schedule import optimize
import unittest
class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(optimize([]),(0,[]))
    def test_adjacent(self): self.assertEqual(optimize([(0,2,3),(2,4,4)])[0],7)
    def test_overlap(self): self.assertEqual(optimize([(0,4,8),(1,3,10)])[0],10)
    def test_global(self): self.assertEqual(optimize([(0,8,12),(0,3,7),(3,8,8)])[0],15)
    def test_bad(self):
        with self.assertRaises(ValueError): optimize([(2,2,1)])
if __name__=="__main__": unittest.main()
