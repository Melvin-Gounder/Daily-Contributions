# Safe Arithmetic Expression Parser

Recursive-descent expression evaluator with precedence, unary signs, parentheses, and explicit errors.

## Usage

Python 3.9+, standard library only. Run `python tool.py` for a demo and `python -m unittest -v test_tool.py` for tests.

## Design and limitations

Recursive-descent grammar: expression -> term (+/- term)*, term -> factor (*// factor)*, factor -> unary, parenthesized expression or decimal. O(n) parsing time and O(n) recursion depth. Uses float arithmetic; not suitable for exact financial calculations. Never executes user input as Python.
