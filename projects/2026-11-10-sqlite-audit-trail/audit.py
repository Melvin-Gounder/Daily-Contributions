"""SQLite inventory CRUD with immutable-by-API trigger audit records."""
import argparse
import json
import sqlite3

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS inventory (
 id INTEGER PRIMARY KEY,
 sku TEXT NOT NULL UNIQUE,
 quantity INTEGER NOT NULL CHECK(quantity >= 0),
 price_cents INTEGER NOT NULL CHECK(price_cents >= 0)
);
CREATE TABLE IF NOT EXISTS audit (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT,
 inventory_id INTEGER NOT NULL,
 action TEXT NOT NULL CHECK(action IN ('INSERT','UPDATE','DELETE')),
 old_state TEXT,
 new_state TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER IF NOT EXISTS inventory_insert AFTER INSERT ON inventory
BEGIN
 INSERT INTO audit(inventory_id, action, new_state)
 VALUES (NEW.id,'INSERT',json_object('sku',NEW.sku,'quantity',NEW.quantity,'price_cents',NEW.price_cents));
END;
CREATE TRIGGER IF NOT EXISTS inventory_update AFTER UPDATE ON inventory
BEGIN
 INSERT INTO audit(inventory_id, action, old_state, new_state)
 VALUES (OLD.id,'UPDATE',
 json_object('sku',OLD.sku,'quantity',OLD.quantity,'price_cents',OLD.price_cents),
 json_object('sku',NEW.sku,'quantity',NEW.quantity,'price_cents',NEW.price_cents));
END;
CREATE TRIGGER IF NOT EXISTS inventory_delete AFTER DELETE ON inventory
BEGIN
 INSERT INTO audit(inventory_id, action, old_state)
 VALUES (OLD.id,'DELETE',json_object('sku',OLD.sku,'quantity',OLD.quantity,'price_cents',OLD.price_cents));
END;
"""

def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db

def add(db, sku, quantity, price_cents):
    with db:
        cursor = db.execute("INSERT INTO inventory(sku,quantity,price_cents) VALUES (?,?,?)",
                            (sku, quantity, price_cents))
    return cursor.lastrowid

def change(db, item_id, *, quantity, price_cents):
    with db:
        cursor = db.execute("UPDATE inventory SET quantity=?,price_cents=? WHERE id=?",
                            (quantity,price_cents,item_id))
        if cursor.rowcount != 1:
            raise KeyError(item_id)

def delete(db, item_id):
    with db:
        cursor=db.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        if cursor.rowcount != 1:
            raise KeyError(item_id)

def history(db, item_id):
    rows=db.execute("SELECT event_id,action,old_state,new_state,created_at FROM audit WHERE inventory_id=? ORDER BY event_id", (item_id,))
    return [{**dict(row),
             "old_state": json.loads(row["old_state"]) if row["old_state"] else None,
             "new_state": json.loads(row["new_state"]) if row["new_state"] else None} for row in rows]

def main():
    parser=argparse.ArgumentParser(description="Trigger-backed SQLite audit demo")
    parser.add_argument("--database",default=":memory:")
    args=parser.parse_args()
    with connect(args.database) as db:
        item=add(db,"ROUTER-01",4,12500)
        change(db,item,quantity=3,price_cents=12500)
        delete(db,item)
        print(json.dumps(history(db,item),indent=2))

if __name__=="__main__":
    main()
