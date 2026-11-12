import unittest
from tool import align,replay
class Tests(unittest.TestCase):
    def test_classic(self):
        d,s=align("kitten","sitting");self.assertEqual(d,3);self.assertEqual(replay("kitten",s),"sitting")
    def test_empty(self):
        for a,b in [("","abc"),("abc",""),("","")]:
            d,s=align(a,b);self.assertEqual(d,max(len(a),len(b)));self.assertEqual(replay(a,s),b)
    def test_unicode(self):
        d,s=align("café","cafe");self.assertEqual(d,1);self.assertEqual(replay("café",s),"cafe")
    def test_identical(self):
        d,s=align("abc","abc");self.assertEqual(d,0);self.assertEqual(replay("abc",s),"abc")
if __name__=="__main__": unittest.main()
