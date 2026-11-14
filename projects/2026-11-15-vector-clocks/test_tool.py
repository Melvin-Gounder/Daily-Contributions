import unittest
from tool import VectorClock, relation

class Tests(unittest.TestCase):
    def test_message_order(self):
        a, b = VectorClock(["a","b"]), VectorClock(["a","b"])
        a.tick("a")
        b.receive("b", a.snapshot())
        self.assertEqual(relation(a.snapshot(), b.snapshot()), "before")
    def test_concurrency(self):
        a, b = VectorClock(["a","b"]), VectorClock(["a","b"])
        a.tick("a"); b.tick("b")
        self.assertEqual(relation(a.snapshot(), b.snapshot()), "concurrent")
    def test_reject_bad_clock(self):
        with self.assertRaises(ValueError): VectorClock(["a","a"])
        with self.assertRaises(ValueError): relation({"a":1},{"b":1})
if __name__ == "__main__": unittest.main()
