import unittest
from tool import top_k
class Tests(unittest.TestCase):
    def test_order(self): self.assertEqual(top_k([("a",2),("b",5),("c",5)],2),[("b",5),("c",5)])
    def test_zero(self): self.assertEqual(top_k([("a",1)],0),[])
    def test_large(self): self.assertEqual(top_k([("a",1)],5),[("a",1)])
    def test_invalid(self):
        with self.assertRaises(ValueError): top_k([("x",float("nan"))],1)
        with self.assertRaises(ValueError): top_k([], -1)
if __name__=="__main__": unittest.main()
