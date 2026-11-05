import unittest
from ring import Ring
class Tests(unittest.TestCase):
 def test_deterministic(self):
  a,b=Ring(16),Ring(16)
  for r in (a,b):
   for n in ("a","b","c"): r.add(n)
  self.assertEqual([a.locate(str(i)) for i in range(100)],[b.locate(str(i)) for i in range(100)])
 def test_minimal_remapping(self):
  r=Ring(32)
  for n in ("a","b","c"): r.add(n)
  before={str(i):r.locate(str(i)) for i in range(300)}
  r.remove("b")
  self.assertTrue(all(r.locate(k)==v for k,v in before.items() if v!="b"))
 def test_errors(self):
  r=Ring()
  with self.assertRaises(LookupError): r.locate("x")
  r.add("a")
  with self.assertRaises(ValueError): r.add("a")
  with self.assertRaises(KeyError): r.remove("z")
 def test_single(self):
  r=Ring(2); r.add("a"); self.assertEqual(r.locate("any"),"a")
if __name__=="__main__": unittest.main()
