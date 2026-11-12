import unittest,sqlite3
from tool import initialize,increment
class Tests(unittest.TestCase):
    def setUp(self): self.c=sqlite3.connect(":memory:");initialize(self.c)
    def tearDown(self): self.c.close()
    def test_replay(self):
        self.assertEqual(increment(self.c,"k","x",2),{"name":"x","value":2})
        self.assertEqual(increment(self.c,"k","x",2),{"name":"x","value":2})
        self.assertEqual(increment(self.c,"j","x",1)["value"],3)
    def test_conflict(self):
        increment(self.c,"k","x")
        with self.assertRaises(ValueError): increment(self.c,"k","x",3)
    def test_validation(self):
        with self.assertRaises(ValueError): increment(self.c,"","x")
    def test_persistence(self):
        self.assertEqual(self.c.execute("SELECT COUNT(*) FROM commands").fetchone()[0],0)
if __name__=="__main__": unittest.main()
