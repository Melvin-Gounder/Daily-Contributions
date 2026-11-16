import unittest
from tool import parallel_map
class Tests(unittest.TestCase):
    def test_order(self):
        out = parallel_map(lambda x: x*x, range(20), workers=3, capacity=2)
        self.assertEqual([o.value for o in out], [x*x for x in range(20)])
    def test_errors(self):
        def f(x):
            if x == 2: raise RuntimeError("bad")
            return x
        out = parallel_map(f, [1,2,3])
        self.assertEqual(out[0].value, 1)
        self.assertIsInstance(out[1].error, RuntimeError)
        self.assertEqual(out[2].value, 3)
    def test_validation(self):
        with self.assertRaises(ValueError): parallel_map(str, [1], workers=0)
if __name__ == "__main__": unittest.main()
