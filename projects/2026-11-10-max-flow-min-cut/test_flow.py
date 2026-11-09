import unittest
from flow import solve

class FlowTests(unittest.TestCase):
    def test_example(self):
        result = solve([("s","a",3),("s","b",2),("a","b",1),("a","t",2),("b","t",3)], "s", "t")
        self.assertEqual(result["max_flow"], 5)
        self.assertEqual(sum(c for _,_,c in result["min_cut"]), 5)
    def test_parallel(self):
        self.assertEqual(solve([("s","t",2),("s","t",4)],"s","t")["max_flow"],6)
    def test_disconnected(self):
        self.assertEqual(solve([("s","a",3)],"s","t")["max_flow"],0)
    def test_reverse_edges(self):
        edges=[("s","a",1),("s","b",1),("a","b",1),("a","t",1),("b","t",1)]
        self.assertEqual(solve(edges,"s","t")["max_flow"],2)
    def test_invalid(self):
        with self.assertRaises(ValueError): solve([("s","t",-1)],"s","t")
        with self.assertRaises(ValueError): solve([],"s","s")
    def test_zero(self):
        self.assertEqual(solve([("s","t",0)],"s","t")["max_flow"],0)

if __name__ == "__main__":
    unittest.main()
