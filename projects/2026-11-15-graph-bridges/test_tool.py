import unittest
from tool import analyze

class Tests(unittest.TestCase):
    def test_triangle_tail(self):
        result=analyze([0,1,2,3],[(0,1),(1,2),(2,0),(1,3)])
        self.assertEqual(result["bridges"],[(1,3)])
        self.assertEqual(result["articulation_points"],[1])
    def test_disconnected(self):
        result=analyze([0,1,2,3],[(0,1),(2,3)])
        self.assertEqual(len(result["bridges"]),2)
        self.assertEqual(result["articulation_points"],[])
    def test_invalid(self):
        with self.assertRaises(ValueError): analyze([0],[(0,1)])
if __name__ == "__main__": unittest.main()
