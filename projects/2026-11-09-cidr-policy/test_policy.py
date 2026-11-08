from policy import Policy
import unittest
class Tests(unittest.TestCase):
    def test_order(self):
        p=Policy([("deny","10.0.0.0/24"),("allow","10.0.0.0/8")])
        self.assertFalse(p.check("10.0.0.1")[0])
        self.assertTrue(p.check("10.2.0.1")[0])
    def test_default(self): self.assertFalse(Policy([]).check("1.1.1.1")[0])
    def test_boundary(self): self.assertFalse(Policy([("allow","10.0.0.0/30")]).check("10.0.0.4")[0])
    def test_bad_network(self):
        with self.assertRaises(ValueError): Policy([("allow","10.0.0.1/24")])
    def test_bad_address(self):
        with self.assertRaises(ValueError): Policy([]).check("999.1.1.1")
if __name__=="__main__": unittest.main()
