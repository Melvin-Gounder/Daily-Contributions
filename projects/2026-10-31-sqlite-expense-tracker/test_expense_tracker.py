import sqlite3
import unittest
from expense_tracker import add_expense, init_db, monthly_summary, parse_money

class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        init_db(self.db)

    def tearDown(self): self.db.close()

    def test_add_and_summary(self):
        add_expense(self.db, "2026-10-01", 1250, "Food", "Lunch")
        add_expense(self.db, "2026-10-02", 750, "food", "Coffee")
        self.assertEqual([("Food", 2000, 2)], [(x.category, x.total_cents, x.transactions) for x in monthly_summary(self.db, "2026-10")])

    def test_month_boundary(self):
        add_expense(self.db, "2026-10-31", 100, "Travel", "Bus")
        add_expense(self.db, "2026-11-01", 200, "Travel", "Taxi")
        self.assertEqual(100, monthly_summary(self.db, "2026-10")[0].total_cents)

    def test_categories_are_case_insensitive(self):
        add_expense(self.db, "2026-10-01", 100, "Books", "A")
        add_expense(self.db, "2026-10-02", 200, "books", "B")
        self.assertEqual(1, self.db.execute("SELECT COUNT(*) FROM categories").fetchone()[0])

    def test_invalid_date_rejected(self):
        with self.assertRaises(ValueError): add_expense(self.db, "2026-02-30", 100, "Food", "x")

    def test_nonpositive_amount_rejected(self):
        with self.assertRaises(ValueError): add_expense(self.db, "2026-10-01", 0, "Food", "x")

    def test_blank_fields_rejected(self):
        with self.assertRaises(ValueError): add_expense(self.db, "2026-10-01", 100, " ", "x")

    def test_money_parser_avoids_float_rounding(self):
        self.assertEqual(1099, parse_money("10.99"))
        with self.assertRaises(ValueError): parse_money("10.999")

    def test_parameterized_input_is_data_not_sql(self):
        payload = "Food'); DROP TABLE expenses; --"
        add_expense(self.db, "2026-10-01", 100, payload, "safe")
        self.assertEqual(1, self.db.execute("SELECT COUNT(*) FROM expenses").fetchone()[0])

if __name__ == "__main__": unittest.main()
