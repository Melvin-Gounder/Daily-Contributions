import unittest
from retry import run

class FixedRng:
    def uniform(self, lo, hi):
        return hi

class RetryTests(unittest.TestCase):
    def test_eventual_success(self):
        calls = []
        def operation():
            calls.append(1)
            if len(calls) < 3:
                raise TimeoutError()
            return 42
        waits = []
        self.assertEqual(run(operation, attempts=3, base=2, cap=3,
                             rng=FixedRng(), sleep=waits.append), 42)
        self.assertEqual(waits, [2, 3])
    def test_exhaustion(self):
        with self.assertRaises(TimeoutError):
            run(lambda: (_ for _ in ()).throw(TimeoutError()), attempts=2,
                sleep=lambda _: None)
    def test_not_retryable(self):
        calls = []
        def fail():
            calls.append(1)
            raise ValueError()
        with self.assertRaises(ValueError):
            run(fail, sleep=lambda _: None)
        self.assertEqual(len(calls), 1)
    def test_validation(self):
        with self.assertRaises(ValueError):
            run(lambda: None, attempts=0)
        with self.assertRaises(ValueError):
            run(lambda: None, cap=-1)

if __name__ == "__main__":
    unittest.main()
