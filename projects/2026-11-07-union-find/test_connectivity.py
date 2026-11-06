import unittest
from connectivity import DisjointSet, redundant_edges

class ConnectivityTests(unittest.TestCase):
    def test_merges_and_sizes(self):
        ds = DisjointSet("abcd")
        self.assertTrue(ds.union("a","b"))
        self.assertTrue(ds.union("b","c"))
        self.assertFalse(ds.union("a","c"))
        self.assertTrue(ds.connected("a","c"))
        self.assertEqual(ds.size[ds.find("a")], 3)
        self.assertFalse(ds.connected("a","d"))
    def test_components(self):
        ds = DisjointSet([1,2,3])
        ds.union(1,2)
        self.assertEqual({frozenset(x) for x in ds.components()},
                         {frozenset([1,2]),frozenset([3])})
    def test_unknown(self):
        with self.assertRaises(KeyError):
            DisjointSet().find("missing")
    def test_cycles(self):
        self.assertEqual(redundant_edges(range(3),[(0,1),(1,2),(2,0),(0,0)]),
                         [(2,0),(0,0)])
    def test_duplicate(self):
        ds = DisjointSet([1])
        self.assertFalse(ds.add(1))
        self.assertTrue(ds.add(2))

if __name__ == "__main__":
    unittest.main()
