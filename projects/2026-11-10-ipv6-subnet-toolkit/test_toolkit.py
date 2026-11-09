import unittest
from toolkit import parse_network, summarize, contains, partition, address_at

class IPv6Tests(unittest.TestCase):
    def test_summary(self):
        self.assertEqual(summarize("2001:db8::/126")["addresses"], 4)
    def test_split(self):
        self.assertEqual(partition("2001:db8::/126", 127), ["2001:db8::/127", "2001:db8::2/127"])
    def test_contains(self):
        self.assertTrue(contains("2001:db8::/126", "2001:db8::3"))
        self.assertFalse(contains("2001:db8::/126", "2001:db8::4"))
        self.assertFalse(contains("2001:db8::/126", "192.0.2.1"))
    def test_offset(self):
        self.assertEqual(address_at("2001:db8::/126", 3), "2001:db8::3")
        with self.assertRaises(ValueError): address_at("2001:db8::/126", 4)
    def test_strict(self):
        with self.assertRaises(ValueError): parse_network("2001:db8::1/64")
    def test_limit(self):
        with self.assertRaises(ValueError): partition("2001:db8::/64", 96)
    def test_prefix(self):
        with self.assertRaises(ValueError): partition("2001:db8::/64", 60)

if __name__ == "__main__":
    unittest.main()
