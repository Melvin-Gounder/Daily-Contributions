import unittest
from tool import checksum,verify
class Tests(unittest.TestCase):
    def test_known(self): self.assertEqual(checksum(bytes.fromhex("0001f203f4f5f6f7")),0x220d)
    def test_empty(self): self.assertEqual(checksum(b""),65535)
    def test_append_even(self):
        payload=b"abcd";tag=checksum(payload).to_bytes(2,"big")
        self.assertTrue(verify(payload+tag))
    def test_odd(self): self.assertEqual(checksum(b"a"),checksum(b"a\x00"))
    def test_type(self):
        with self.assertRaises(TypeError): checksum("hello")
if __name__=="__main__": unittest.main()
