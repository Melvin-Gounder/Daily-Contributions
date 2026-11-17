# Matrix Chain Multiplication Optimizer

Dynamic programming for minimum scalar multiplications with parenthesization reconstruction and dimension validation.

## Usage

Python 3.9+, standard library only. Run `python tool.py` for a classic example, or `python -m unittest -v test_tool.py` for six tests.

## Algorithm

Given matrix dimensions p0...pn, compute minimum multiplication cost C[i,j] over split points k: C[i,k] + C[k+1,j] + p[i]*p[k+1]*p[j+1]. Reconstruct the optimal parenthesization from split points. O(n³) time and O(n²) space. The tool plans multiplication order; it does not multiply matrices.
