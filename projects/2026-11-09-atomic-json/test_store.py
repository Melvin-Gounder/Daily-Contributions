from store import Store,ConflictError
import unittest,tempfile
from pathlib import Path
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.s=Store(Path(self.tmp.name)/"sub"/"store.json")
    def test_missing(self): self.assertEqual(self.s.read()["revision"],0)
    def test_roundtrip(self):
        self.assertEqual(self.s.write({"a":1},0),1)
        self.assertEqual(self.s.read()["data"],{"a":1})
    def test_conflict(self):
        self.s.write({"a":1},0)
        with self.assertRaises(ConflictError): self.s.write({"a":2},0)
        self.assertEqual(self.s.read()["data"],{"a":1})
    def test_invalid(self):
        with self.assertRaises(ValueError): self.s.write({"x":float("nan")},0)
    def test_type(self):
        with self.assertRaises(TypeError): self.s.write([],0)
if __name__=="__main__": unittest.main()
