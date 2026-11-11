import unittest
from totp import hotp, totp, verify

SECRET=b"12345678901234567890"

class TotpTests(unittest.TestCase):
    def test_rfc6238_vector_59(self):
        self.assertEqual(totp(SECRET,at=59,digits=8),"94287082")
    def test_rfc6238_vector_1111111109(self):
        self.assertEqual(totp(SECRET,at=1111111109,digits=8),"07081804")
    def test_hotp_rfc4226(self):
        self.assertEqual(hotp(SECRET,0),"755224")
    def test_verify(self):
        code=totp(SECRET,at=120)
        self.assertTrue(verify(SECRET,code,at=120,window=0))
        self.assertFalse(verify(SECRET,"abcdef",at=120))
    def test_bad_step(self):
        with self.assertRaises(ValueError): totp(SECRET,at=10,step=0)

if __name__ == "__main__":
    unittest.main()
