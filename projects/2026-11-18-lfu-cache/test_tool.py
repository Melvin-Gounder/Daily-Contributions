import unittest
from tool import LFUCache
class Tests(unittest.TestCase):
    def test_frequency(self):
        c=LFUCache(2);c.put("a",1);c.put("b",2);c.get("a");c.put("c",3)
        self.assertIsNone(c.get("b"));self.assertEqual(c.get("a"),1)
    def test_tie(self):
        c=LFUCache(2);c.put("a",1);c.put("b",2);c.put("c",3)
        self.assertIsNone(c.get("a"))
    def test_update(self):
        c=LFUCache(2);c.put("a",1);c.put("b",2);c.put("a",3);c.put("c",4)
        self.assertEqual(c.get("a"),3)
    def test_zero(self):
        c=LFUCache(0);c.put("a",1);self.assertFalse(c.values)
    def test_bad(self):
        with self.assertRaises(ValueError): LFUCache(-1)
if __name__=="__main__": unittest.main()
