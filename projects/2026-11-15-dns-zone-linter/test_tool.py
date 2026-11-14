import unittest
from tool import lint

class Tests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(lint([("example.org","A","192.0.2.1"),("mail.example.org","MX","10 example.org"),("v6.example.org","AAAA","2001:db8::1")]),[])
    def test_conflicting_alias(self):
        self.assertTrue(any("coexist" in e for e in lint([("x.org","CNAME","y.org"),("x.org","A","192.0.2.1")])))
    def test_bad_family(self):
        self.assertTrue(lint([("x.org","AAAA","192.0.2.1")]))
    def test_bad_host(self):
        self.assertTrue(lint([("-bad.org","A","192.0.2.1")]))
if __name__ == "__main__": unittest.main()
