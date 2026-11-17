import unittest
from tool import root,proof,verify
class Tests(unittest.TestCase):
    def test_every_leaf(self):
        items=[b"a",b"b",b"c",b"d",b"e"]
        for i,x in enumerate(items): self.assertTrue(verify(x,proof(items,i),root(items)))
    def test_tampering(self):
        x=[b"a",b"b",b"c"]
        self.assertFalse(verify(b"wrong",proof(x,1),root(x)))
    def test_single(self):
        self.assertTrue(verify(b"a",[],root([b"a"])))
    def test_empty(self):
        with self.assertRaises(ValueError): root([])
    def test_bad_index(self):
        with self.assertRaises(IndexError): proof([b"a"],2)
if __name__=="__main__": unittest.main()
