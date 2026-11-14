import csv
import io
import unittest
from tool import transform, pseudonym

class Tests(unittest.TestCase):
    def test_stability(self):
        self.assertEqual(pseudonym(b"secret", "alice"),pseudonym(b"secret","alice"))
        self.assertNotEqual(pseudonym(b"secret","alice"),pseudonym(b"secret","bob"))
    def test_csv(self):
        src=csv.DictReader(io.StringIO("name,city\nalice,Suva\nbob,Nadi\n"))
        out=io.StringIO()
        transform(src,csv.DictWriter(out,fieldnames=src.fieldnames),["name"],b"secret")
        self.assertIn("Suva",out.getvalue())
        self.assertNotIn("alice",out.getvalue())
    def test_missing(self):
        src=csv.DictReader(io.StringIO("name\na\n"))
        with self.assertRaises(ValueError):
            transform(src,csv.DictWriter(io.StringIO(),fieldnames=["name"]),["email"],b"secret")
if __name__ == "__main__": unittest.main()
