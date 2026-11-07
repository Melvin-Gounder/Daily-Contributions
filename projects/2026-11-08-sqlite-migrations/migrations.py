import sqlite3,hashlib
MIGRATIONS=((1,"CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE)"),(2,"CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), total_cents INTEGER NOT NULL CHECK(total_cents>=0))"),(3,"CREATE INDEX orders_customer_idx ON orders(customer_id)"))
class MigrationError(Exception): pass
def migrate(db,migrations=MIGRATIONS):
    versions=[v for v,_ in migrations]
    if versions!=list(range(1,len(versions)+1)): raise MigrationError("noncontiguous versions")
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, checksum TEXT NOT NULL)")
    old=dict(db.execute("SELECT version,checksum FROM schema_migrations")); known=dict(migrations)
    for v,checksum in old.items():
        if v not in known or hashlib.sha256(known[v].encode()).hexdigest()!=checksum: raise MigrationError("history drift")
    db.commit(); done=[]
    for v,sql in migrations:
        if v in old: continue
        try:
            db.execute("BEGIN IMMEDIATE")
            db.execute(sql)
            db.execute("INSERT INTO schema_migrations VALUES (?,?)",(v,hashlib.sha256(sql.encode()).hexdigest()))
            db.commit();done.append(v)
        except sqlite3.Error as exc:
            db.rollback();raise MigrationError(str(exc)) from exc
    return done
if __name__=="__main__":
    db=sqlite3.connect(":memory:");print(migrate(db));print(migrate(db))
