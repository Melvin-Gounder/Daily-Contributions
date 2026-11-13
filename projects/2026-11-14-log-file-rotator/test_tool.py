import tempfile
import unittest
from pathlib import Path
from tool import RotatingLog

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"app.log"
    def test_rotation(self):
        log=RotatingLog(self.path,6,2)
        for x in ["aa","bb","cc","dd"]: log.write(x)
        self.assertEqual(self.path.read_text(),"cc\ndd\n")
        self.assertEqual(Path(str(self.path)+".1").read_text(),"aa\nbb\n")
    def test_oversize(self):
        with self.assertRaises(ValueError): RotatingLog(self.path,2).write("hello")
    def test_no_backups(self):
        log=RotatingLog(self.path,3,0)
        log.write("aa"); log.write("bb")
        self.assertEqual(self.path.read_text(),"bb\n")
if __name__=="__main__": unittest.main()
