import unittest
from tool import shortest_paths, path_to

class Tests(unittest.TestCase):
    def test_negative_edge(self):
        d, p = shortest_paths("ABCD", [("A","B",4),("A","C",5),("B","C",-2),("C","D",3)], "A")
        self.assertEqual(d["D"], 5)
        self.assertEqual(path_to(p, "A", "D"), ["A","B","C","D"])
    def test_unreachable(self):
        d, p = shortest_paths("ABC", [("A","B",1)], "A")
        self.assertEqual(d["C"], float("inf"))
        self.assertIsNone(path_to(p, "A", "C"))
    def test_cycle(self):
        with self.assertRaisesRegex(ValueError, "negative-weight"):
            shortest_paths("ABC", [("A","B",1),("B","C",-3),("C","B",1)], "A")
    def test_unreachable_cycle_ignored(self):
        d, _ = shortest_paths("ABCD", [("A","B",2),("C","D",-3),("D","C",1)], "A")
        self.assertEqual(d["B"], 2)
    def test_bad_source(self):
        with self.assertRaises(ValueError):
            shortest_paths("AB", [], "Z")

if __name__ == "__main__":
    unittest.main()
