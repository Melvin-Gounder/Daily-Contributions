import unittest
from tool import redact
class Tests(unittest.TestCase):
    def test_nested(self):
        x={"Auth":[{"TOKEN":"abc","ok":True}],"password":"x"}
        y=redact(x);self.assertEqual(y["Auth"][0]["TOKEN"],"[REDACTED]");self.assertEqual(x["password"],"x")
    def test_custom(self): self.assertEqual(redact({"pin":"1234"},["PIN"])["pin"],"[REDACTED]")
    def test_cycle(self):
        x=[];x.append(x)
        with self.assertRaises(ValueError): redact(x)
    def test_bad_type(self):
        with self.assertRaises(TypeError): redact({"x":object()})
if __name__=="__main__": unittest.main()
