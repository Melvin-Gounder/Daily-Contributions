"""Retry transient failures with bounded exponential backoff (stdlib only)."""
from dataclasses import dataclass
from typing import Callable
import random
import time

@dataclass(frozen=True)
class Attempt:
    number: int
    delay_after: float

def run(operation: Callable, *, attempts=4, base=0.2, cap=5.0,
        retry_on=(TimeoutError, ConnectionError), sleep=time.sleep,
        rng=None, on_retry=None):
    """Return operation result or raise its final exception.

    Full jitter draws uniformly from [0, min(cap, base * 2**(n-1))].
    Never retries non-retryable errors. All waits occur AFTER a failure.
    """
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    if base < 0 or cap < 0:
        raise ValueError("delays cannot be negative")
    if not isinstance(retry_on, tuple) or not retry_on or not all(
        isinstance(t, type) and issubclass(t, Exception) for t in retry_on
    ):
        raise ValueError("retry_on must be a tuple of exception classes")
    rng = rng or random.Random()
    for number in range(1, attempts + 1):
        try:
            return operation()
        except retry_on:
            if number == attempts:
                raise
            delay = rng.uniform(0, min(cap, base * 2 ** min(number - 1, 1024)))
            if on_retry:
                on_retry(Attempt(number, delay))
            sleep(delay)

if __name__ == "__main__":
    failures = iter([TimeoutError("temporary"), TimeoutError("temporary"), "ok"])
    print(run(lambda: (lambda x: x if isinstance(x, str) else (_ for _ in ()).throw(x))(next(failures)),
              sleep=lambda seconds: print("waiting", round(seconds, 3)),
              rng=random.Random(7)))
