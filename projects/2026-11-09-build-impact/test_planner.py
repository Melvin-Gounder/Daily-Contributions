from planner import plan,CycleError
import unittest
class Tests(unittest.TestCase):
    def setUp(self): self.g={"lib":[],"app":["lib"],"docs":[],"ship":["app","docs"]}
    def test_full(self):
        order=plan(self.g)
        for n,ds in self.g.items():
            for d in ds: self.assertLess(order.index(d),order.index(n))
    def test_incremental(self): self.assertEqual(plan(self.g,["lib"]),["lib","app","ship"])
    def test_independent(self): self.assertEqual(plan(self.g,["docs"]),["docs","ship"])
    def test_empty(self): self.assertEqual(plan({}),[])
    def test_unknown(self):
        with self.assertRaises(ValueError): plan({"a":["missing"]})
    def test_cycle(self):
        with self.assertRaises(CycleError): plan({"a":["b"],"b":["a"]})
if __name__=="__main__": unittest.main()
