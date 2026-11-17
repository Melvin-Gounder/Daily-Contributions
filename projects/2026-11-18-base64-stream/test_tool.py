import io
import unittest
from tool import encode,decode
class Tests(unittest.TestCase):
    def roundtrip(self,data,chunk):
        encoded=io.BytesIO()
        encode(io.BytesIO(data),encoded,chunk)
        output=io.BytesIO()
        decode(io.BytesIO(encoded.getvalue()),output,chunk)
        self.assertEqual(output.getvalue(),data)
    def test_empty(self): self.roundtrip(b"",5)
    def test_small(self): self.roundtrip(b"hello",1)
    def test_large(self): self.roundtrip(bytes(range(256))*12,7)
    def test_invalid(self):
        with self.assertRaises(Exception): decode(io.BytesIO(b"!!!!"),io.BytesIO(),4)
    def test_truncated(self):
        with self.assertRaises(ValueError): decode(io.BytesIO(b"YQ"),io.BytesIO(),3)
if __name__=="__main__": unittest.main()
