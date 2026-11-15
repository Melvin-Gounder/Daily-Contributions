import tempfile
import unittest
from pathlib import Path
from tool import sort_file
class Tests(unittest.TestCase):
    def test_multi_run(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d)/"input", Path(d)/"output"
            src.write_text("9\n-1\n5\n5\n0\n2\n", encoding="utf-8")
            sort_file(str(src),str(dst),2)
            self.assertEqual(dst.read_text(encoding="utf-8"),"-1\n0\n2\n5\n5\n9\n")
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            src,dst=Path(d)/"i",Path(d)/"o"
            src.write_text("",encoding="utf-8")
            sort_file(str(src),str(dst))
            self.assertEqual(dst.read_text(encoding="utf-8"),"")
    def test_failure_preserves_output(self):
        with tempfile.TemporaryDirectory() as d:
            src,dst=Path(d)/"i",Path(d)/"o"
            src.write_text("2\ninvalid\n",encoding="utf-8")
            dst.write_text("original",encoding="utf-8")
            with self.assertRaises(ValueError): sort_file(str(src),str(dst),1)
            self.assertEqual(dst.read_text(encoding="utf-8"),"original")
if __name__ == "__main__": unittest.main()
