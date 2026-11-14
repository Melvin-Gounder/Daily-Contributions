import unittest
from tool import evolve, stationary_estimate, validate

class Tests(unittest.TestCase):
    def test_swap(self):
        self.assertEqual(evolve([[0,1],[1,0]],[1,0],3),[0,1])
    def test_stationary(self):
        state, _ = stationary_estimate([[.9,.1],[.4,.6]])
        self.assertAlmostEqual(state[0],.8,places=6)
    def test_invalid(self):
        with self.assertRaises(ValueError): validate([[.2,.2],[.5,.5]])
    def test_periodic(self):
        with self.assertRaises(RuntimeError): stationary_estimate([[0,1],[1,0]],max_steps=10)
if __name__ == "__main__": unittest.main()
