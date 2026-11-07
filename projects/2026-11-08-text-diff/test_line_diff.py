import unittest
from line_diff import diff,apply
class Tests(unittest.TestCase):
 def test_reconstruction(self):
  a=["a","b","c"];b=["a","x","c","d"];e=diff(a,b)
  self.assertEqual(apply(a,e),b);self.assertEqual(sum(op==" " for op,_ in e),2)
 def test_empty(self):self.assertEqual(diff([],[]),[]);self.assertEqual(apply([],diff([],["x"])),["x"])
 def test_duplicates(self):
  a=["a","b","a"];b=["b","a","a"];self.assertEqual(apply(a,diff(a,b)),b)
 def test_mismatch(self):
  with self.assertRaises(ValueError):apply(["old"],[(" ","wrong")])
if __name__=="__main__":unittest.main()
