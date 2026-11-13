import unittest
from tool import transitive_reduction

class Tests(unittest.TestCase):
    def test_redundant(self):
        self.assertEqual(transitive_reduction({"a":["b","c"],"b":["c"]}),{"a":("b",),"b":("c",),"c":()})
    def test_diamond(self):
        g={"a":["b","c","d"],"b":["d"],"c":["d"]}
        self.assertEqual(transitive_reduction(g)["a"],("b","c"))
    def test_cycle(self):
        with self.assertRaises(ValueError): transitive_reduction({"a":["b"],"b":["a"]})
    def test_empty(self): self.assertEqual(transitive_reduction({}),{})
if __name__=="__main__": unittest.main()
