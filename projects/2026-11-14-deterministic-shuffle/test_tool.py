import unittest
from tool import shuffle,HashStream

class Tests(unittest.TestCase):
    def test_permutation(self):
        a=list(range(100))
        self.assertEqual(sorted(shuffle(a,"seed")),a)
        self.assertEqual(a,list(range(100)))
    def test_repeatable(self):
        self.assertEqual(shuffle(list(range(20)),"abc"),shuffle(list(range(20)),"abc"))
    def test_edge_cases(self):
        self.assertEqual(shuffle([],"x"),[])
        self.assertEqual(shuffle([5],"x"),[5])
        with self.assertRaises(ValueError): HashStream("x").randbelow(0)
if __name__=="__main__": unittest.main()
