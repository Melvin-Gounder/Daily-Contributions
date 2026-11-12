import unittest
from tool import solve
class Tests(unittest.TestCase):
    def test_matching_and_cover(self):
        g={"a":[1,2],"b":[2],"c":[1]}
        matching,(left,right)=solve(g)
        self.assertEqual(len(matching),2);self.assertEqual(len(left)+len(right),2)
        self.assertTrue(all(u in left or v in right for u,vs in g.items() for v in vs))
    def test_empty(self): self.assertEqual(solve({}),({},(set(),set())))
    def test_disconnected(self):
        m,_=solve({"a":[],"b":[1],"c":[2]});self.assertEqual(len(m),2)
    def test_no_duplicate_assignment(self):
        m,_=solve({"a":[1,1],"b":[1]});self.assertEqual(len(set(m.values())),len(m))
if __name__=="__main__": unittest.main()
