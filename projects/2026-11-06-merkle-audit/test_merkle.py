import unittest
from merkle import root,proof,verify
class Tests(unittest.TestCase):
 def test_all_sizes(self):
  for n in range(1,9):
   batch=[str(i).encode() for i in range(n)]
   for i,v in enumerate(batch): self.assertTrue(verify(v,proof(batch,i),root(batch)))
 def test_tamper(self):
  b=[b"a",b"b",b"c"]
  self.assertFalse(verify(b"x",proof(b,1),root(b)))
  self.assertFalse(verify(b"b",proof(b,1),"0"*64))
 def test_order(self): self.assertNotEqual(root([b"a",b"b"]),root([b"b",b"a"]))
 def test_errors(self):
  with self.assertRaises(ValueError): root([])
  with self.assertRaises(IndexError): proof([b"a"],1)
  self.assertFalse(verify(b"a",[("right","zz")],"0"*64))
if __name__=="__main__": unittest.main()
