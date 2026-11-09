import sqlite3
import unittest
from audit import connect,add,change,delete,history

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.db=connect()
        self.addCleanup(self.db.close)
    def test_lifecycle(self):
        item=add(self.db,"A",2,99)
        change(self.db,item,quantity=3,price_cents=100)
        delete(self.db,item)
        rows=history(self.db,item)
        self.assertEqual([r["action"] for r in rows],["INSERT","UPDATE","DELETE"])
        self.assertEqual(rows[1]["old_state"]["quantity"],2)
        self.assertEqual(rows[2]["old_state"]["price_cents"],100)
    def test_rollback_on_invalid_update(self):
        item=add(self.db,"B",2,100)
        with self.assertRaises(sqlite3.IntegrityError):
            change(self.db,item,quantity=-1,price_cents=100)
        self.assertEqual(len(history(self.db,item)),1)
    def test_duplicate_sku(self):
        add(self.db,"A",1,1)
        with self.assertRaises(sqlite3.IntegrityError): add(self.db,"A",2,2)
    def test_missing(self):
        with self.assertRaises(KeyError): change(self.db,999,quantity=1,price_cents=1)
    def test_sql_parameterization(self):
        item=add(self.db,"x'); DROP TABLE inventory; --",1,1)
        self.assertEqual(history(self.db,item)[0]["new_state"]["sku"],"x'); DROP TABLE inventory; --")
    def test_delete_missing(self):
        with self.assertRaises(KeyError): delete(self.db,999)

if __name__=="__main__":
    unittest.main()
