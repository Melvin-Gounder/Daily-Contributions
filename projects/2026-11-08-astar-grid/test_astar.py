import unittest
from astar import path
class Tests(unittest.TestCase):
 def test_detour(self):
  p,c=path([[0,0,0],[1,1,0],[0,0,0]],(0,0),(2,0))
  self.assertEqual(c,6);self.assertEqual((p[0],p[-1]),((0,0),(2,0)))
 def test_unreachable(self): self.assertEqual(path([[0,1],[1,0]],(0,0),(1,1)),([],None))
 def test_identity(self): self.assertEqual(path([[0]],(0,0),(0,0)),([(0,0)],0))
 def test_invalid(self):
  with self.assertRaises(ValueError): path([[1]],(0,0),(0,0))
if __name__=="__main__": unittest.main()
