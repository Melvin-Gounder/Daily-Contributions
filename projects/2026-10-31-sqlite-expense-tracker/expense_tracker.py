"""SQLite-backed expense tracker using only Python's standard library."""
from __future__ import annotations
import argparse
import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS categories(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE COLLATE NOCASE
);
CREATE TABLE IF NOT EXISTS expenses(
  id INTEGER PRIMARY KEY,
  spent_on TEXT NOT NULL CHECK(spent_on GLOB '????-??-??'),
  amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
  description TEXT NOT NULL,
  category_id INTEGER NOT NULL REFERENCES categories(id)
);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(spent_on);
CREATE INDEX IF NOT EXISTS idx_expenses_category_date ON expenses(category_id, spent_on);
"""

@dataclass(frozen=True)
class Summary:
    category: str
    total_cents: int
    transactions: int


def connect(path: str | Path) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db(db: sqlite3.Connection) -> None:
    db.executescript(SCHEMA)
    db.commit()


def add_expense(db: sqlite3.Connection, spent_on: str, amount_cents: int,
                category: str, description: str) -> int:
    date.fromisoformat(spent_on)  # strict calendar validation
    category, description = category.strip(), description.strip()
    if amount_cents <= 0 or not category or not description:
        raise ValueError("amount must be positive; category/description cannot be blank")
    with db:  # atomic transaction; rolls back automatically on failure
        db.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (category,))
        category_id = db.execute(
            "SELECT id FROM categories WHERE name = ? COLLATE NOCASE", (category,)
        ).fetchone()[0]
        cursor = db.execute(
            "INSERT INTO expenses(spent_on, amount_cents, description, category_id) VALUES (?,?,?,?)",
            (spent_on, amount_cents, description, category_id),
        )
    return int(cursor.lastrowid)


def monthly_summary(db: sqlite3.Connection, month: str) -> list[Summary]:
    if len(month) != 7:
        raise ValueError("month must be YYYY-MM")
    date.fromisoformat(month + "-01")
    rows = db.execute("""
        SELECT c.name AS category, SUM(e.amount_cents) AS total, COUNT(*) AS n
        FROM expenses e JOIN categories c ON c.id = e.category_id
        WHERE e.spent_on >= ? AND e.spent_on < date(?, '+1 month')
        GROUP BY c.id, c.name ORDER BY total DESC, c.name
    """, (month + "-01", month + "-01")).fetchall()
    return [Summary(r["category"], r["total"], r["n"]) for r in rows]


def parse_money(text: str) -> int:
    from decimal import Decimal, InvalidOperation
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("invalid amount") from exc
    cents = value * 100
    if value <= 0 or cents != cents.to_integral_value():
        raise ValueError("amount must be positive with at most 2 decimal places")
    return int(cents)


def main() -> int:
    parser = argparse.ArgumentParser(description="Local SQLite expense tracker")
    parser.add_argument("--db", default="expenses.db")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("date"); add.add_argument("amount"); add.add_argument("category"); add.add_argument("description")
    report = sub.add_parser("report"); report.add_argument("month")
    args = parser.parse_args()
    with connect(args.db) as db:
        init_db(db)
        if args.command == "add":
            expense_id = add_expense(db, args.date, parse_money(args.amount), args.category, args.description)
            print(f"Added expense #{expense_id}")
        else:
            rows = monthly_summary(db, args.month)
            total = sum(r.total_cents for r in rows)
            for r in rows:
                print(f"{r.category:20} ${r.total_cents/100:9.2f}  ({r.transactions})")
            print(f"{'TOTAL':20} ${total/100:9.2f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
