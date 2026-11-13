import tempfile
import unittest
from pathlib import Path
from tool import profile

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"data.csv"
    def test_stats(self):
        self.path.write_text("age,city\n2,Suva\n,\n4,Nadi\n",encoding="utf-8")
        result=profile(self.path)
        self.assertEqual(result["rows"],3)
        self.assertEqual(result["columns"]["age"]["missing"],1)
        self.assertEqual(result["columns"]["age"]["min"],2)
        self.assertEqual(result["columns"]["age"]["inferred_type"],"number")
    def test_ragged(self):
        self.path.write_text("a,b\n1\n")
        with self.assertRaises(ValueError): profile(self.path)
    def test_duplicate_header(self):
        self.path.write_text("a,a\n1,2\n")
        with self.assertRaises(ValueError): profile(self.path)
if __name__=="__main__": unittest.main()
