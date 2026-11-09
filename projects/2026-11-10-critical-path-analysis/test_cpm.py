import unittest
from cpm import Activity,analyze

class CPMTests(unittest.TestCase):
    def test_project(self):
        result=analyze({"a":Activity(3),"b":Activity(5,("a",)),
                        "c":Activity(2,("a",)),"d":Activity(1,("b","c"))})
        self.assertEqual(result["duration"],9)
        self.assertEqual(result["critical"],["a","b","d"])
        self.assertEqual(result["activities"]["c"]["slack"],3)
    def test_parallel(self):
        result=analyze({"a":Activity(2),"b":Activity(4)})
        self.assertEqual(result["duration"],4)
        self.assertEqual(result["activities"]["a"]["slack"],2)
    def test_empty(self):
        self.assertEqual(analyze({})["duration"],0)
    def test_cycle(self):
        with self.assertRaises(ValueError):
            analyze({"a":Activity(1,("b",)),"b":Activity(1,("a",))})
    def test_missing(self):
        with self.assertRaises(ValueError): analyze({"a":Activity(1,("z",))})
    def test_negative(self):
        with self.assertRaises(ValueError): analyze({"a":Activity(-1)})
    def test_zero(self):
        self.assertEqual(analyze({"a":Activity(0)})["duration"],0)
    def test_duplicate_dependency(self):
        with self.assertRaises(ValueError): analyze({"a":Activity(1),"b":Activity(1,("a","a"))})

if __name__=="__main__":
    unittest.main()
