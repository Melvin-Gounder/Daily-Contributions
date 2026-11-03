import unittest
from subnet import describe, split

class SubnetTests(unittest.TestCase):
    def test_normal(self):
        d = describe("192.168.10.44/24")
        self.assertEqual((d["network"], d["broadcast"]), ("192.168.10.0", "192.168.10.255"))
        self.assertEqual((d["first_usable"], d["last_usable"], d["usable_hosts"]), ("192.168.10.1", "192.168.10.254", 254))
    def test_point_to_point(self):
        self.assertEqual(describe("10.0.0.0/31")["usable_hosts"], 2)
    def test_single_host(self):
        self.assertEqual(describe("10.0.0.5/32")["first_usable"], "10.0.0.5")
    def test_split(self):
        self.assertEqual(split("10.0.0.0/24", 26), ["10.0.0.0/26","10.0.0.64/26","10.0.0.128/26","10.0.0.192/26"])
    def test_invalid(self):
        with self.assertRaises(ValueError): split("10.0.0.0/24", 23)
        with self.assertRaises(ValueError): describe("300.0.0.0/24")

if __name__ == "__main__": unittest.main()
