import unittest
from polynomial import Polynomial

class PolynomialTests(unittest.TestCase):
    def test_cancellation(self):
        self.assertEqual(Polynomial({1: 2}) + Polynomial({1: -2}), Polynomial())
    def test_product(self):
        p = Polynomial({1: 1, 0: 1})
        self.assertEqual(p*p, Polynomial({2: 1, 1: 2, 0: 1}))
    def test_derivative(self):
        self.assertEqual(Polynomial({3: 2, 0: 5}).derivative(), Polynomial({2: 6}))
    def test_fraction(self):
        self.assertEqual(Polynomial({1: "1/2"}).evaluate("3/2"), "3/4")
    def test_invalid_degree(self):
        with self.assertRaises(ValueError): Polynomial({-1: 2})

if __name__ == "__main__":
    unittest.main()
