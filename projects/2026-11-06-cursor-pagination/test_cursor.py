import unittest
from cursor import encode,decode,page,InvalidCursor
KEY=b"test-secret-with-adequate-length"
class Tests(unittest.TestCase):
 def test_roundtrip(self):
  for n in (0,1,2**60): self.assertEqual(decode(encode(n,KEY),KEY),n)
 def test_pages(self):
  rows=[(i,str(i)) for i in range(10)]; token=None; found=[]
  while True:
   batch,token=page(rows,3,KEY,token); found+=batch
   if token is None: break
  self.assertEqual(found,rows)
 def test_tampering(self):
  token=encode(7,KEY)
  with self.assertRaises(InvalidCursor): decode(token+"!",KEY)
  with self.assertRaises(InvalidCursor): decode(token,b"another-secret-long-enough")
 def test_validation(self):
  with self.assertRaises(ValueError): page([(2,"a"),(1,"b")],1,KEY)
  with self.assertRaises(ValueError): page([],0,KEY)
 def test_empty(self): self.assertEqual(page([],2,KEY),([],None))
if __name__=="__main__": unittest.main()
