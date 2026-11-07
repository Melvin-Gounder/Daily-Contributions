import unittest
from webhook import Verifier,WebhookError,signature
class Tests(unittest.TestCase):
 def setUp(self):self.v=Verifier(b"key",clock=lambda:1000)
 def test_valid_replay(self):
  s=signature(b"key",1000,b"body")
  self.assertTrue(self.v.verify(1000,b"body",s))
  with self.assertRaises(WebhookError):self.v.verify(1000,b"body",s)
 def test_tamper(self):
  with self.assertRaises(WebhookError):self.v.verify(1000,b"changed",signature(b"key",1000,b"body"))
 def test_expiry(self):
  with self.assertRaises(WebhookError):self.v.verify(699,b"body",signature(b"key",699,b"body"))
 def test_boundary(self):self.assertTrue(self.v.verify(700,b"body",signature(b"key",700,b"body")))
if __name__=="__main__":unittest.main()
