import unittest
from tool import codebook,encode,decode
class Tests(unittest.TestCase):
    def test_roundtrip(self):
        codes=codebook({"A":5,"B":2,"C":1,"D":1})
        self.assertEqual(decode(encode("ABCDDA",codes),codes),"ABCDDA")
        self.assertTrue(all(not b.startswith(a) for x,a in codes.items() for y,b in codes.items() if x!=y))
    def test_single(self):
        codes=codebook({"X":1});self.assertEqual(decode(encode("XXX",codes),codes),"XXX")
    def test_determinism(self):
        self.assertEqual(codebook({"b":1,"a":1}),codebook({"a":1,"b":1}))
    def test_invalid(self):
        with self.assertRaises(ValueError): codebook({"A":0})
if __name__=="__main__": unittest.main()
