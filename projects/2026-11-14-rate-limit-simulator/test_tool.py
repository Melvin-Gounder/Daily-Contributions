import unittest
from tool import TokenBucket

class Clock:
    now=0.0
    def __call__(self): return self.now

class Tests(unittest.TestCase):
    def test_refill(self):
        c=Clock(); b=TokenBucket(2,1,c)
        self.assertTrue(b.acquire()[0]); self.assertTrue(b.acquire()[0])
        ok,wait=b.acquire(); self.assertFalse(ok); self.assertAlmostEqual(wait,1)
        c.now=0.5; self.assertFalse(b.acquire()[0])
        c.now=1; self.assertTrue(b.acquire()[0])
    def test_cap_and_errors(self):
        c=Clock(); b=TokenBucket(2,1,c)
        c.now=100
        self.assertTrue(b.acquire(2)[0])
        with self.assertRaises(ValueError): b.acquire(3)
        c.now=99
        with self.assertRaises(ValueError): b.acquire()
if __name__=="__main__": unittest.main()
