import unittest
from tool import Index, tokenize
class Tests(unittest.TestCase):
    def test_phrase_vs_and(self):
        x = Index()
        x.put("a", "red blue green")
        x.put("b", "blue red")
        self.assertEqual(x.search_all("red blue"), ["a", "b"])
        self.assertEqual(x.phrase("red blue"), ["a"])
    def test_replace_and_remove(self):
        x = Index()
        x.put(1, "one")
        x.put(1, "two")
        self.assertEqual(x.search_all("one"), [])
        x.remove(1)
        self.assertEqual(x.search_all("two"), [])
    def test_unicode(self):
        self.assertEqual(tokenize("CAFÉ café"), ["café", "café"])
if __name__ == "__main__": unittest.main()
