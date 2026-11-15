import unittest
from tool import find_all
class Tests(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(find_all("aaaa", "aa"), [0,1,2])
        self.assertEqual(find_all("bananana", "ana"), [1,3,5])
    def test_unicode(self):
        self.assertEqual(find_all("🍎🍐🍎", "🍎"), [0,2])
    def test_empty(self):
        self.assertEqual(find_all("abc", ""), [0,1,2,3])
        self.assertEqual(find_all("ab", "abcd"), [])
    def test_collision(self):
        self.assertEqual(find_all("abcabc", "bc", modulus=2), [1,4])
    def test_invalid(self):
        with self.assertRaises(ValueError): find_all("a","a", modulus=1)
if __name__ == "__main__": unittest.main()
