import tempfile
import unittest
from pathlib import Path
from tool import reconcile
class Tests(unittest.TestCase):
    def test_changes(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/"a.csv", Path(d)/"b.csv"
            a.write_text("id,value\n1,a\n2,b\n", encoding="utf-8")
            b.write_text("id,value\n2,c\n3,d\n", encoding="utf-8")
            result = reconcile(a, b, "id")
            self.assertEqual(list(result["added"]), ["3"])
            self.assertEqual(list(result["removed"]), ["1"])
            self.assertEqual(result["modified"]["2"]["value"], {"old":"b","new":"c"})
    def test_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            a = Path(d)/"a.csv"
            a.write_text("id,x\n1,a\n1,b\n", encoding="utf-8")
            with self.assertRaises(ValueError): reconcile(a, a, "id")
if __name__ == "__main__": unittest.main()
