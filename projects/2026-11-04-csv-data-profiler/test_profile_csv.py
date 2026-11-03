import os
import tempfile
import unittest
from profile_csv import profile

class ProfileTests(unittest.TestCase):
    def check(self, content):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False) as file:
            file.write(content)
            path = file.name
        try: return profile(path)
        finally: os.unlink(path)
    def test_numbers(self):
        result = self.check("name,score\nAda,10\nBob,20\n")
        self.assertEqual(result["columns"]["score"]["numeric_mean"], "15")
        self.assertEqual(result["rows"], 2)
    def test_missing(self):
        self.assertEqual(self.check("x,y\n,1\n2,\n")["columns"]["x"]["missing"], 1)
    def test_malformed(self):
        self.assertEqual(self.check("x,y\n1\n1,2,3\n")["malformed_rows"], 2)
    def test_duplicate_headers(self):
        with self.assertRaises(ValueError): self.check("x,x\n1,2\n")
    def test_nonfinite(self):
        self.assertEqual(self.check("x\nNaN\nInfinity\n")["columns"]["x"]["numeric_count"], 0)

if __name__ == "__main__": unittest.main()
