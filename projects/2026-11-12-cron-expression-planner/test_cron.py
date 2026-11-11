import unittest
from datetime import datetime
from cron import Cron, parse_field

class CronTests(unittest.TestCase):
    def test_step(self):
        self.assertEqual(parse_field("*/20",0,59), {0,20,40})
    def test_ranges_and_list(self):
        self.assertEqual(parse_field("1-3,8",0,10), {1,2,3,8})
    def test_weekday(self):
        self.assertTrue(Cron("0 9 * * 4").matches(datetime(2026,11,12,9,0)))
    def test_next(self):
        self.assertEqual(Cron("0 9 * * *").next_after(datetime(2026,11,12,9,0)), datetime(2026,11,13,9,0))
    def test_reject(self):
        with self.assertRaises(ValueError): Cron("60 * * * *")
    def test_or_semantics(self):
        self.assertTrue(Cron("0 9 1 * 4").matches(datetime(2026,11,12,9,0)))

if __name__ == "__main__":
    unittest.main()
