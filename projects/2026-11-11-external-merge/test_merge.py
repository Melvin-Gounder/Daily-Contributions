import tempfile
import unittest
from pathlib import Path
from merge import merge,merge_to_file
class TestMerge(unittest.TestCase):
    def test_duplicates_and_negative(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"a"; b=Path(d)/"b"
            a.write_text("-3\n1\n4\n"); b.write_text("-3\n2\n4\n")
            self.assertEqual(list(merge([a,b])),[-3,-3,1,2,4,4])
            out=Path(d)/"out"; merge_to_file([a,b],out)
            self.assertEqual(out.read_text(),"-3\n-3\n1\n2\n4\n4\n")
    def test_unsorted(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a"; p.write_text("2\n1\n")
            with self.assertRaises(ValueError): list(merge([p]))
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a"; p.write_text("1\n")
            with self.assertRaises(ValueError): merge_to_file([p],p)
if __name__=="__main__": unittest.main()
