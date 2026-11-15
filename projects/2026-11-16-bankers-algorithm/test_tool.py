import unittest
from tool import safety, request
class Tests(unittest.TestCase):
    def setUp(self):
        self.av = [3,3,2]
        self.al = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
        self.mx = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
    def test_safe(self):
        safe, seq = safety(self.av,self.al,self.mx)
        self.assertTrue(safe)
        self.assertEqual(len(set(seq)), 5)
    def test_request(self):
        self.assertTrue(request(self.av,self.al,self.mx,1,[1,0,2])[0])
        self.assertEqual(self.av,[3,3,2])
    def test_unsafe(self):
        self.assertFalse(safety([0],[[1],[1]],[[2],[2]])[0])
    def test_bad(self):
        with self.assertRaises(ValueError): safety([1],[[2]],[[1]])
if __name__ == "__main__": unittest.main()
