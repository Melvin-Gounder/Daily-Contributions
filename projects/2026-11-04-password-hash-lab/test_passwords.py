import unittest
from passwords import hash_password, verify_password, needs_rehash

class PasswordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stored = hash_password("pássword", iterations=100_000)
    def test_valid(self): self.assertTrue(verify_password("pássword", self.stored))
    def test_invalid(self): self.assertFalse(verify_password("wrong", self.stored))
    def test_unicode(self): self.assertFalse(verify_password("password", self.stored))
    def test_unique_salts(self):
        self.assertNotEqual(hash_password("same", 100_000), hash_password("same", 100_000))
    def test_malformed(self):
        self.assertFalse(verify_password("x", "broken"))
        self.assertFalse(verify_password("x", "pbkdf2_sha256$999999999999999$AA==$AA=="))
    def test_rehash(self):
        self.assertTrue(needs_rehash(self.stored))
        self.assertFalse(needs_rehash(self.stored, 100_000))
    def test_empty(self):
        with self.assertRaises(ValueError): hash_password("")

if __name__ == "__main__": unittest.main()
