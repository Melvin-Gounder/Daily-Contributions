"""Finite Markov-chain evolution using row-stochastic matrices."""
import math

def validate(matrix):
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("square nonempty matrix required")
    for row in matrix:
        if any(not math.isfinite(x) or x < 0 for x in row) or not math.isclose(sum(row),1,abs_tol=1e-10):
            raise ValueError("rows must be probability distributions")
    return n

def step(matrix, distribution):
    n = validate(matrix)
    if len(distribution) != n or any(not math.isfinite(x) or x < 0 for x in distribution) or not math.isclose(sum(distribution),1,abs_tol=1e-10):
        raise ValueError("invalid starting distribution")
    return [sum(distribution[i] * matrix[i][j] for i in range(n)) for j in range(n)]

def evolve(matrix, distribution, steps):
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be nonnegative integer")
    validate(matrix)
    if len(distribution) != len(matrix) or any(not math.isfinite(x) or x < 0 for x in distribution) or not math.isclose(sum(distribution),1,abs_tol=1e-10):
        raise ValueError("invalid starting distribution")
    state = list(distribution)
    for _ in range(steps):
        state = step(matrix, state)
    return state

def stationary_estimate(matrix, tolerance=1e-9, max_steps=10000):
    n = validate(matrix)
    if tolerance <= 0 or max_steps < 1:
        raise ValueError("invalid convergence settings")
    state = [1/n] * n
    for iteration in range(1, max_steps+1):
        next_state = step(matrix, state)
        if max(abs(a-b) for a,b in zip(state,next_state)) < tolerance:
            return next_state, iteration
        state = next_state
    raise RuntimeError("did not converge; chain may be periodic or reducible")

if __name__ == "__main__":
    print(stationary_estimate([[0.9,0.1],[0.4,0.6]]))
