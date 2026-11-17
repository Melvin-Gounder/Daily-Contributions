import unittest
from tool import bucket,key_hash,assign
class Tests(unittest.TestCase):
    def test_bounds(self):
        for n in range(1,40):
            for k in range(200): self.assertTrue(0<=bucket(k,n)<n)
    def test_growth_moves_only_to_new_bucket(self):
        for n in range(1,20):
            for k in range(100):
                old,new=bucket(k,n),bucket(k,n+1)
                self.assertIn(new,(old,n))
    def test_repeatable(self): self.assertEqual(assign("hello",8),assign("hello",8))
    def test_invalid(self):
        with self.assertRaises(ValueError): bucket(-1,3)
        with self.assertRaises(ValueError): bucket(1,0)
    def test_hash(self): self.assertEqual(key_hash("x"),key_hash("x"))
if __name__=="__main__": unittest.main()
