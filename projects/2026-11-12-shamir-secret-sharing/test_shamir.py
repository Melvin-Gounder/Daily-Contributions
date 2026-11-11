import unittest
from shamir import split, recover, PRIME

class SecretTests(unittest.TestCase):
    def test_any_threshold_subset(self):
        from itertools import combinations
        shares = split(987654,3,5)
        for subset in combinations(shares,3):
            self.assertEqual(recover(subset),987654)
    def test_duplicate(self):
        s=split(10,2,3)
        with self.assertRaises(ValueError): recover([s[0],s[0]])
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError): split(5,1,3)
    def test_large_secret(self):
        s=split(PRIME-1,2,2)
        self.assertEqual(recover(s), PRIME-1)

if __name__ == "__main__":
    unittest.main()
