import unittest
from tool import resolve,tokens
class Tests(unittest.TestCase):
    def test_root(self): self.assertEqual(resolve({"x":1},""),{"x":1})
    def test_escape(self): self.assertEqual(resolve({"a/b":{"~":4}},"/a~1b/~0"),4)
    def test_array(self): self.assertEqual(resolve([10,20],"/1"),20)
    def test_bad_index(self):
        with self.assertRaises(IndexError): resolve([1],"/01")
    def test_missing(self):
        with self.assertRaises(KeyError): resolve({},"/x")
    def test_invalid_escape(self):
        with self.assertRaises(ValueError): tokens("/~3")
if __name__=="__main__": unittest.main()
