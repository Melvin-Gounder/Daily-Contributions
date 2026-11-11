import unittest
from ranges import parse_range, RangeNotSatisfiable

class RangeTests(unittest.TestCase):
    def test_bounded(self):
        self.assertEqual(parse_range("bytes=10-19",100).length,10)
    def test_open_ended(self):
        self.assertEqual(parse_range("bytes=90-",100).content_range,"bytes 90-99/100")
    def test_suffix(self):
        self.assertEqual(parse_range("bytes=-200",100).length,100)
    def test_clamp(self):
        self.assertEqual(parse_range("bytes=5-100",10).end,9)
    def test_unsatisfiable(self):
        with self.assertRaises(RangeNotSatisfiable): parse_range("bytes=10-",10)
    def test_multipart_rejected(self):
        with self.assertRaises(ValueError): parse_range("bytes=0-1,3-4",100)

if __name__ == "__main__":
    unittest.main()
