import unittest
from search import SearchIndex,tokenize
class TestSearch(unittest.TestCase):
    def test_tokens(self): self.assertEqual(tokenize("Hello, WORLD!"),["hello","world"])
    def test_rank(self):
        i=SearchIndex(); i.add("a","python python testing"); i.add("b","java testing")
        self.assertEqual(i.search("python")[0][0],"a")
        self.assertEqual(i.search("missing"),[])
    def test_replace_remove(self):
        i=SearchIndex(); i.add("x","old"); i.add("x","new")
        self.assertEqual(i.search("old"),[])
        i.remove("x"); self.assertEqual(i.search("new"),[])
    def test_validation(self):
        with self.assertRaises(ValueError): SearchIndex(b=2)
if __name__=="__main__": unittest.main()
