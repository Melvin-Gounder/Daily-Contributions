from cache import evaluate,parse
import unittest
class Tests(unittest.TestCase):
    def test_fresh(self): self.assertTrue(evaluate("max-age=60",59).fresh)
    def test_boundary(self): self.assertFalse(evaluate("max-age=60",60).fresh)
    def test_no_store(self): self.assertFalse(evaluate("no-store, max-age=60",0).storable)
    def test_no_cache(self):
        d=evaluate("no-cache, max-age=60",0)
        self.assertTrue(d.storable); self.assertFalse(d.fresh)
    def test_private(self): self.assertFalse(evaluate("private, max-age=60",0).storable)
    def test_private_local(self): self.assertTrue(evaluate("private, max-age=60",0,shared=False).storable)
    def test_shared(self): self.assertFalse(evaluate("max-age=90, s-maxage=10",10).fresh)
    def test_auth(self): self.assertFalse(evaluate("max-age=60",0,authenticated=True).storable)
    def test_bad(self):
        with self.assertRaises(ValueError): evaluate("max-age=bad",0)
if __name__=="__main__": unittest.main()
