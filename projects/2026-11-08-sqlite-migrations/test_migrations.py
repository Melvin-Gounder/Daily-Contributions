import sqlite3,unittest
from migrations import migrate,MigrationError,MIGRATIONS
class Tests(unittest.TestCase):
 def setUp(self): self.db=sqlite3.connect(":memory:")
 def tearDown(self): self.db.close()
 def test_idempotent(self):
  self.assertEqual(migrate(self.db),[1,2,3]);self.assertEqual(migrate(self.db),[])
 def test_foreign_key(self):
  migrate(self.db)
  with self.assertRaises(sqlite3.IntegrityError): self.db.execute("INSERT INTO orders VALUES (1,999,100)")
 def test_drift(self):
  migrate(self.db)
  with self.assertRaises(MigrationError): migrate(self.db,((1,"SELECT 1"),)+MIGRATIONS[1:])
 def test_rollback(self):
  with self.assertRaises(MigrationError): migrate(self.db,((1,"CREATE TABLE x(id INTEGER)"),(2,"CREATE TABLE x(id INTEGER)")))
  self.assertEqual(self.db.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0],1)
if __name__=="__main__": unittest.main()
