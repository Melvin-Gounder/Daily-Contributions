import unittest
from scheduler import Scheduler
class Tests(unittest.TestCase):
 def test_eventual_service(self):
  s=Scheduler({"a":1,"b":3}); s.enqueue("a","big",7); s.enqueue("b","small",1)
  self.assertEqual(set(s.drain()),{("a","big"),("b","small")})
 def test_fifo(self):
  s=Scheduler({"a":2,"b":1})
  for i in range(5): s.enqueue("a",i,1)
  self.assertEqual([v for k,v in s.drain()],list(range(5)))
 def test_interleave(self):
  s=Scheduler({"a":1,"b":1})
  for i in range(3): s.enqueue("a",i,1); s.enqueue("b",i,1)
  self.assertEqual([k for k,v in s.drain()],["a","b"]*3)
 def test_errors(self):
  with self.assertRaises(ValueError): Scheduler({"a":0})
  s=Scheduler({"a":1})
  with self.assertRaises(ValueError): s.enqueue("a","bad",0)
  with self.assertRaises(KeyError): s.enqueue("missing","x",1)
if __name__=="__main__": unittest.main()
