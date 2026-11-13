import unittest
from collections import Counter
from tool import SmoothWeightedRoundRobin

class Tests(unittest.TestCase):
    def test_distribution(self):
        s=SmoothWeightedRoundRobin({"a":5,"b":1,"c":1})
        self.assertEqual(Counter(s.next() for _ in range(7)),Counter({"a":5,"b":1,"c":1}))
    def test_updates(self):
        s=SmoothWeightedRoundRobin({"a":1,"b":0})
        self.assertEqual(s.next(),"a")
        s.set_weight("a",0); s.set_weight("b",2)
        self.assertEqual(s.next(),"b")
    def test_invalid(self):
        with self.assertRaises(ValueError): SmoothWeightedRoundRobin({"a":-1})
        with self.assertRaises(ValueError): SmoothWeightedRoundRobin({}).next()
if __name__=="__main__": unittest.main()
