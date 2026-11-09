import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZipInfo
from safezip import extract, UnsafeArchive

class ZipTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.archive=self.root/"a.zip"
        self.dest=self.root/"out"
    def build(self, entries):
        with ZipFile(self.archive,"w") as z:
            for name,data in entries:
                z.writestr(name,data)
    def test_normal(self):
        self.build([("docs/a.txt","hello"),("docs/b.txt","world")])
        self.assertEqual(len(extract(self.archive,self.dest)),2)
        self.assertEqual((self.dest/"docs/a.txt").read_text(),"hello")
    def test_traversal(self):
        self.build([("../escape.txt","bad")])
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest)
    def test_absolute(self):
        self.build([("/tmp/escape","bad")])
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest)
    def test_budget(self):
        self.build([("x.txt","123456")])
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest,max_file=5)
    def test_duplicate(self):
        self.build([("x","a"),("x","b")])
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest)
    def test_existing(self):
        self.build([("x","a")])
        self.dest.mkdir()
        (self.dest/"x").write_text("original")
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest)
        self.assertEqual((self.dest/"x").read_text(),"original")
    def test_symlink_entry(self):
        info=ZipInfo("link")
        info.create_system=3
        info.external_attr=(0o120777 << 16)
        with ZipFile(self.archive,"w") as z: z.writestr(info,"target")
        with self.assertRaises(UnsafeArchive): extract(self.archive,self.dest)

if __name__ == "__main__":
    unittest.main()
