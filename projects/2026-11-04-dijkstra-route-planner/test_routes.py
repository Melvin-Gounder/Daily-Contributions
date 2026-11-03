import math
import unittest
from routes import shortest_paths

class RouteTests(unittest.TestCase):
    def test_shortest(self):
        r = shortest_paths({"A":{"B":10,"C":2},"C":{"B":3},"B":{}}, "A")
        self.assertEqual(r["B"], {"distance":5,"path":["A","C","B"]})
    def test_unreachable(self):
        r = shortest_paths({"A":{},"B":{}}, "A")
        self.assertTrue(math.isinf(r["B"]["distance"]))
        self.assertIsNone(r["B"]["path"])
    def test_zero_weight(self):
        self.assertEqual(shortest_paths({"A":{"B":0}}, "A")["B"]["distance"], 0)
    def test_negative(self):
        with self.assertRaises(ValueError): shortest_paths({"A":{"B":-1}}, "A")
    def test_missing_start(self):
        with self.assertRaises(ValueError): shortest_paths({"A":{}}, "X")
    def test_tie(self):
        r = shortest_paths({"A":{"C":1,"B":1},"B":{"D":1},"C":{"D":1}}, "A")
        self.assertEqual(r["D"]["path"], ["A","B","D"])

if __name__ == "__main__": unittest.main()
