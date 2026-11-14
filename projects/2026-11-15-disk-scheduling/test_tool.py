import unittest
from tool import schedule

class Tests(unittest.TestCase):
    def test_fcfs(self):
        self.assertEqual(schedule([10,20],0,100)["movement"],20)
    def test_sstf(self):
        self.assertEqual(schedule([10,90,12],11,100,"sstf")["order"],[10,12,90])
    def test_scan(self):
        self.assertEqual(schedule([10,80],50,100,"scan")["order"],[80,99,10])
    def test_reject(self):
        with self.assertRaises(ValueError): schedule([100],0,100)
if __name__ == "__main__": unittest.main()
