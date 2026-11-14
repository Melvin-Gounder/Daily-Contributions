import sqlite3
import unittest
from tool import initialize, enqueue, claim, acknowledge

class Tests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(":memory:")
        initialize(self.db)
    def tearDown(self): self.db.close()
    def test_claim_ack(self):
        job=enqueue(self.db,{"a":1})
        self.assertEqual(claim(self.db,now=0),(job,{"a":1}))
        self.assertIsNone(claim(self.db,now=1))
        self.assertTrue(acknowledge(self.db,job,now=1))
        self.assertIsNone(claim(self.db,now=40))
    def test_recovery(self):
        job=enqueue(self.db,"work")
        self.assertEqual(claim(self.db,now=0,lease_seconds=5)[0],job)
        self.assertEqual(claim(self.db,now=5)[0],job)
        self.assertFalse(acknowledge(self.db,job,now=100))
    def test_empty(self):
        self.assertIsNone(claim(self.db,now=0))
if __name__ == "__main__": unittest.main()
