"""Integrity manifest CLI. python integrity.py create DIR MANIFEST; verify DIR MANIFEST; test."""
import hashlib, json, argparse, sys, unittest, tempfile
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(65536),b""): h.update(block)
    return h.hexdigest()

def scan(directory):
    root=Path(directory).resolve()
    if not root.is_dir(): raise ValueError("directory required")
    files={}
    for p in sorted(root.rglob("*")):
        if p.is_symlink(): continue
        if p.is_file(): files[p.relative_to(root).as_posix()]=sha256(p)
    return files

def compare(expected, actual):
    return {"added":sorted(actual.keys()-expected.keys()),
            "removed":sorted(expected.keys()-actual.keys()),
            "modified":sorted(k for k in expected.keys()&actual.keys()
                              if expected[k]!=actual[k])}

class Tests(unittest.TestCase):
    def test_changes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a"
            p.write_text("hello")
            original=scan(d)
            self.assertFalse(any(compare(original,scan(d)).values()))
            p.write_text("changed")
            (Path(d)/"b").write_text("new")
            report=compare(original,scan(d))
            self.assertEqual(report["modified"],["a"])
            self.assertEqual(report["added"],["b"])
            p.unlink()
            self.assertEqual(compare(original,scan(d))["removed"],["a"])
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d: self.assertEqual(scan(d),{})
    def test_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x"
            p.write_bytes(b"abc")
            self.assertEqual(sha256(p),hashlib.sha256(b"abc").hexdigest())

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["create","verify"])
    parser.add_argument("directory")
    parser.add_argument("manifest")
    args=parser.parse_args()
    output=Path(args.manifest).resolve()
    if output.is_relative_to(Path(args.directory).resolve()):
        parser.error("manifest must be outside audited directory")
    if args.action=="create":
        output.write_text(json.dumps(scan(args.directory),indent=2,sort_keys=True)+"\n")
        return 0
    report=compare(json.loads(output.read_text()),scan(args.directory))
    print(json.dumps(report,indent=2))
    return int(any(report.values()))

if __name__=="__main__":
    if sys.argv[1:]==["test"]: unittest.main(argv=[sys.argv[0]])
    else: sys.exit(main())
