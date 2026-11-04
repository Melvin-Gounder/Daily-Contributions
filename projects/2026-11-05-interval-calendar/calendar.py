"""Booking calendar: python calendar.py [test]. Half-open intervals allow adjacent bookings."""
from dataclasses import dataclass
from datetime import datetime, timedelta
import unittest, sys

@dataclass(frozen=True)
class Booking:
    start: datetime
    end: datetime
    label: str
    def __post_init__(self):
        if self.start >= self.end or not self.label.strip():
            raise ValueError("invalid booking")

class Calendar:
    def __init__(self): self.bookings = []
    def add(self, booking):
        if any(booking.start < b.end and b.start < booking.end for b in self.bookings):
            raise ValueError("overlap")
        self.bookings.append(booking)
        self.bookings.sort(key=lambda b: b.start)
    def cancel(self, label):
        for i, b in enumerate(self.bookings):
            if b.label == label: return self.bookings.pop(i)
        raise KeyError(label)
    def free(self, start, end, minimum=timedelta(minutes=30)):
        if start >= end or minimum <= timedelta(): raise ValueError("invalid query")
        cursor, gaps = start, []
        for b in self.bookings:
            if b.end <= cursor: continue
            if b.start >= end: break
            stop = min(end, b.start)
            if stop-cursor >= minimum: gaps.append((cursor, stop))
            cursor = max(cursor, b.end)
        if end-cursor >= minimum: gaps.append((cursor,end))
        return gaps

class Tests(unittest.TestCase):
    def setUp(self):
        self.c=Calendar()
        self.t=lambda h: datetime(2026,11,5,h)
    def test_adjacent(self):
        self.c.add(Booking(self.t(9),self.t(10),"a"))
        self.c.add(Booking(self.t(10),self.t(11),"b"))
        self.assertEqual(len(self.c.bookings),2)
    def test_overlap(self):
        self.c.add(Booking(self.t(9),self.t(11),"a"))
        with self.assertRaises(ValueError):
            self.c.add(Booking(self.t(10),self.t(12),"b"))
    def test_free(self):
        self.c.add(Booking(self.t(10),self.t(11),"a"))
        self.assertEqual(self.c.free(self.t(9),self.t(12)),
                         [(self.t(9),self.t(10)),(self.t(11),self.t(12))])
    def test_cancel(self):
        self.c.add(Booking(self.t(9),self.t(10),"a"))
        self.c.cancel("a")
        self.assertEqual(self.c.bookings,[])

if __name__=="__main__":
    if sys.argv[1:]==["test"]: unittest.main(argv=[sys.argv[0]])
    else:
        c=Calendar()
        c.add(Booking(datetime(2026,11,5,10),datetime(2026,11,5,11),"Meeting"))
        print(c.free(datetime(2026,11,5,9),datetime(2026,11,5,13)))
