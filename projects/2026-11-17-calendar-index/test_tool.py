import unittest
from tool import Calendar

class CalendarTests(unittest.TestCase):
    def test_adjacent_and_conflict(self):
        c = Calendar()
        c.add(1, 3, "a")
        c.add(3, 5, "b")
        with self.assertRaises(ValueError):
            c.add(2, 4, "conflict")
        self.assertEqual(list(c.free_slots(0, 7, 1)), [(0, 1), (5, 7)])
    def test_cancel(self):
        c = Calendar()
        c.add(1, 3, "a")
        c.cancel("a")
        self.assertEqual(list(c.free_slots(0, 4, 2)), [(0, 4)])
    def test_invalid(self):
        with self.assertRaises(ValueError):
            Calendar().add(3, 3, "x")

if __name__ == "__main__":
    unittest.main()
