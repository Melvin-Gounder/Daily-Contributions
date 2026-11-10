import unittest
from scc import analyze
class TestSCC(unittest.TestCase):
    def test_groups(self):
        x=analyze({"a":["b"],"b":["a","c"],"c":["d"],"d":["c"]})
        self.assertEqual(x["components"],[("a","b"),("c","d")])
        self.assertEqual(x["edges"],[(0,1)])
    def test_self_loop(self):
        self.assertEqual(analyze({"x":["x"]})["cyclic"],[("x",)])
    def test_empty(self):
        self.assertEqual(analyze({})["components"],[])
    def test_missing_target(self):
        self.assertEqual(analyze({"a":["b"]})["components"],[("a",),("b",)])
if __name__=="__main__": unittest.main()
