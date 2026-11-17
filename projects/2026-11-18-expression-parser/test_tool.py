import unittest
from tool import evaluate
class Tests(unittest.TestCase):
    def test_precedence(self): self.assertEqual(evaluate("2+3*4"),14)
    def test_parentheses(self): self.assertEqual(evaluate("(2+3)*4"),20)
    def test_unary(self): self.assertEqual(evaluate("-(-2)+3"),5)
    def test_fraction(self): self.assertEqual(evaluate("1/4+0.5"),0.75)
    def test_bad_character(self):
        with self.assertRaises(ValueError): evaluate("2**3")
    def test_zero(self):
        with self.assertRaises(ZeroDivisionError): evaluate("1/0")
    def test_trailing(self):
        with self.assertRaises(ValueError): evaluate("1 2")
if __name__=="__main__": unittest.main()
