import unittest
from tool import evaluate, parse_etags
class Tests(unittest.TestCase):
    def test_weak_read(self):
        self.assertEqual(evaluate("GET", '"a"', if_none_match='W/"a"'), 304)
        self.assertEqual(evaluate("PUT", '"a"', if_none_match='W/"a"'), 412)
    def test_strong_write(self):
        self.assertEqual(evaluate("PUT", '"a"', if_match='W/"a"'), 412)
        self.assertEqual(evaluate("PUT", '"a"', if_match='"a"'), 200)
    def test_missing(self):
        self.assertEqual(evaluate("GET", None, if_match="*"), 412)
        self.assertEqual(evaluate("GET", None, if_none_match="*"), 200)
    def test_invalid(self):
        with self.assertRaises(ValueError): parse_etags("abc")
if __name__ == "__main__": unittest.main()
