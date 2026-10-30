# SQLite Expense Tracker

A dependency-free Python CLI that demonstrates practical relational-database design rather than storing records in an ad-hoc text file.

## What it demonstrates

- normalized `categories` and `expenses` tables with a foreign key;
- `CHECK`, `UNIQUE`, and `NOT NULL` constraints as database-level invariants;
- indexes chosen for date reports and category/date access patterns;
- parameterized SQL, so user text is never concatenated into queries;
- atomic writes with Python's SQLite transaction context manager;
- integer cents and `Decimal` parsing to avoid binary floating-point errors for money;
- grouped monthly reporting with `JOIN`, `SUM`, and `COUNT`;
- in-memory integration tests against a real SQLite engine.

## Run

Requires Python 3.10+; SQLite is included with standard CPython builds.

```bash
cd projects/2026-10-31-sqlite-expense-tracker
python expense_tracker.py --db demo.db add 2026-10-31 12.50 Food "Lunch"
python expense_tracker.py --db demo.db add 2026-10-31 4.20 Travel "Bus fare"
python expense_tracker.py --db demo.db report 2026-10
```

Example report:

```text
Food                 $    12.50  (1)
Travel               $     4.20  (1)
TOTAL                $    16.70
```

## Tests

```bash
python -m unittest -v test_expense_tracker.py
```

Eight tests cover aggregation, month boundaries, case-insensitive category uniqueness, invalid dates/amounts, blank fields, exact money parsing, and a SQL-injection-shaped input to verify parameterization.

## Design notes

Amounts are stored as integer cents, making addition exact. Categories live in their own table so spelling/casing rules and future category metadata have one home. Foreign keys prevent orphaned expenses. The `(category_id, spent_on)` composite index supports category histories, while the date index supports range reports.

SQLite transactions are ACID; the `with db:` block commits the category lookup/creation and expense insert together, or rolls the transaction back if an exception occurs. For a larger application, schema migrations, richer currencies, recurring transactions, authentication, backups, and concurrent-write strategy would be separate concerns.

## Complexity

Database complexity depends on SQLite's query planner and data distribution. B-tree indexes generally avoid a full-table scan for indexed range/equality predicates. The monthly aggregation still processes the matching rows, so indexes reduce row discovery cost but cannot eliminate the work of aggregating returned records.
