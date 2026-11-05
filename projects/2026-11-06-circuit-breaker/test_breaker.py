import unittest
from breaker import Breaker,State,CircuitOpen
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=[0]; self.b=Breaker(2,10,lambda:self.t[0])
 def fail(self): raise OSError("down")
 def test_recovery(self):
  for _ in range(2):
   with self.assertRaises(OSError): self.b.call(self.fail)
  self.assertEqual(self.b.state,State.OPEN)
  with self.assertRaises(CircuitOpen): self.b.call(lambda:1)
  self.t[0]=10
  self.assertEqual(self.b.call(lambda:7),7)
  self.assertEqual(self.b.state,State.CLOSED)
 def test_failed_probe(self):
  for _ in range(2):
   with self.assertRaises(OSError): self.b.call(self.fail)
  self.t[0]=10
  with self.assertRaises(OSError): self.b.call(self.fail)
  self.assertEqual(self.b.opened,10)
 def test_reset(self):
  with self.assertRaises(OSError): self.b.call(self.fail)
  self.b.call(lambda:None); self.assertEqual(self.b.failures,0)
 def test_validation(self):
  with self.assertRaises(ValueError): Breaker(0)
if __name__=="__main__": unittest.main()
