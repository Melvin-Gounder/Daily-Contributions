import json
import tempfile
import unittest
from pathlib import Path
from dedup import deduplicate

class DedupTests(unittest.TestCase):
    def test_first_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/"a.jsonl",Path(tmp)/"b.jsonl"
            a.write_text('{"user":{"id":1},"v":"first"}\n{"user":{"id":1},"v":"second"}\n{"user":{"id":2}}\n')
            self.assertEqual(deduplicate(a,b,"user.id"),(2,1))
            self.assertEqual([json.loads(x)["user"]["id"] for x in b.read_text().splitlines()],[1,2])
    def test_failure_keeps_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/"a",Path(tmp)/"b"
            a.write_text('{"x":1}\nnot-json\n')
            b.write_text("original")
            with self.assertRaises(ValueError): deduplicate(a,b,"x")
            self.assertEqual(b.read_text(),"original")
    def test_same_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"x"
            with self.assertRaises(ValueError): deduplicate(p,p,"id")

if __name__ == "__main__":
    unittest.main()
