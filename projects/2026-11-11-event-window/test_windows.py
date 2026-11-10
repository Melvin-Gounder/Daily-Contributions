import unittest
from windows import Aggregator,Window
class TestWindows(unittest.TestCase):
    def test_out_of_order(self):
        a=Aggregator(10); self.assertTrue(a.add(9,2)); a.add(1,3); a.add(12,5)
        self.assertEqual(a.advance(10),[Window(0,10,2,5)])
        self.assertEqual(a.advance(20),[Window(10,20,1,5)])
    def test_late(self):
        a=Aggregator(5); a.advance(10); self.assertFalse(a.add(1,4))
    def test_negative_timestamp(self):
        a=Aggregator(10); a.add(-1,7)
        self.assertEqual(a.advance(0)[0].start,-10)
    def test_invalid(self):
        with self.assertRaises(ValueError): Aggregator(0)
if __name__=="__main__": unittest.main()
