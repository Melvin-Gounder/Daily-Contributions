import unittest
from tool import Decoder, FrameError, encode
class Tests(unittest.TestCase):
    def test_fragmented_and_multiple(self):
        d = Decoder()
        raw = encode(b"abc") + encode(b"") + encode(b"xyz")
        self.assertEqual(d.feed(raw[:5]), [])
        self.assertEqual(d.feed(raw[5:]), [b"abc", b"", b"xyz"])
        d.finish()
    def test_maximum(self):
        with self.assertRaises(FrameError):
            Decoder(2).feed(encode(b"abc")[:4])
    def test_truncated(self):
        d = Decoder()
        d.feed(encode(b"hi")[:-1])
        with self.assertRaises(FrameError):
            d.finish()
if __name__ == "__main__": unittest.main()
