import unittest
from tool import resolve,ConfigurationError

class Tests(unittest.TestCase):
    def test_nested(self):
        self.assertEqual(resolve("${URL}",{"URL":"https://${HOST}","HOST":"example.org"}),"https://example.org")
    def test_default(self):
        self.assertEqual(resolve("${PORT:-8080}",{}),"8080")
    def test_missing(self):
        with self.assertRaises(ConfigurationError): resolve("${X}",{})
    def test_cycle(self):
        with self.assertRaises(ConfigurationError): resolve("${A}",{"A":"${B}","B":"${A}"})
    def test_no_execution(self):
        self.assertEqual(resolve("$(echo bad)",{}),"$(echo bad)")
if __name__=="__main__": unittest.main()
