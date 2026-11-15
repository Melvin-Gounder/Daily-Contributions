import unittest
from tool import Store
class Tests(unittest.TestCase):
    def test_snapshots(self):
        s = Store()
        self.assertEqual(s.snapshot(), 0)
        s.put("a", 1)
        old = s.snapshot()
        s.put("a", 2)
        s.delete("a")
        self.assertEqual(s.get("a", old), 1)
        self.assertIsNone(s.get("a"))
        self.assertEqual(s.get("a", 2), 2)
    def test_scan(self):
        s = Store()
        s.put("b", 2)
        s.put("a", 1)
        snap = s.snapshot()
        s.delete("b")
        self.assertEqual(s.scan(snap), {"a":1, "b":2})
        self.assertEqual(s.scan(), {"a":1})
    def test_invalid(self):
        s = Store()
        with self.assertRaises(ValueError): s.get("x", 1)
if __name__ == "__main__": unittest.main()
