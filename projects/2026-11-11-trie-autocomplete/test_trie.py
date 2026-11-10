import unittest
from trie import Autocomplete
class TestTrie(unittest.TestCase):
    def test_ranking(self):
        t=Autocomplete(); t.set("cat",2); t.set("car",4); t.set("cap",4)
        self.assertEqual([w for w,_ in t.suggest("ca")],["cap","car","cat"])
    def test_delete_and_update(self):
        t=Autocomplete(); t.set("a",1); t.set("ab",2)
        self.assertTrue(t.delete("a")); self.assertEqual(t.suggest("a"),[("ab",2)])
        t.set("ab",5); self.assertEqual(t.suggest("ab"),[("ab",5)])
    def test_missing(self): self.assertFalse(Autocomplete().delete("x"))
    def test_invalid(self):
        with self.assertRaises(ValueError): Autocomplete().set("",1)
if __name__=="__main__": unittest.main()
