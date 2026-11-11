from fractions import Fraction

class Polynomial:
    """Sparse univariate polynomial with exact rational coefficients."""
    def __init__(self, terms=None):
        self.terms = {}
        for degree, coefficient in (terms or {}).items():
            if not isinstance(degree, int) or degree < 0:
                raise ValueError("degrees must be nonnegative integers")
            value = Fraction(coefficient)
            if value:
                self.terms[degree] = value

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        terms = self.terms.copy()
        for degree, coefficient in other.terms.items():
            terms[degree] = terms.get(degree, Fraction(0)) + coefficient
        return Polynomial(terms)

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        terms = {}
        for a, x in self.terms.items():
            for b, y in other.terms.items():
                terms[a+b] = terms.get(a+b, Fraction(0)) + x*y
        return Polynomial(terms)

    def derivative(self):
        return Polynomial({d-1: d*c for d,c in self.terms.items() if d})

    def evaluate(self, x):
        x = Fraction(x)
        return sum((c * x**d for d,c in self.terms.items()), Fraction(0))

    def __eq__(self, other):
        return isinstance(other, Polynomial) and self.terms == other.terms

    def __repr__(self):
        return f"Polynomial({self.terms!r})"

if __name__ == "__main__":
    p = Polynomial({2: 1, 1: -2, 0: 1})
    print("p(3) =", p.evaluate(3), "; p'(3) =", p.derivative().evaluate(3))
