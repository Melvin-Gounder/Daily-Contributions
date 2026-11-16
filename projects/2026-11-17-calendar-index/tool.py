"""Deterministic interval overlap index for calendar conflict detection."""
from bisect import bisect_left
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Booking:
    start: int
    end: int
    name: str

class Calendar:
    def __init__(self):
        self._bookings = []

    def add(self, start: int, end: int, name: str):
        if not isinstance(start, int) or not isinstance(end, int) or start >= end:
            raise ValueError("expected integer half-open interval with start < end")
        if not name or any(b.name == name for b in self._bookings):
            raise ValueError("booking name must be nonempty and unique")
        booking = Booking(start, end, name)
        index = bisect_left(self._bookings, booking)
        if index and self._bookings[index - 1].end > start:
            raise ValueError("overlaps previous booking")
        if index < len(self._bookings) and self._bookings[index].start < end:
            raise ValueError("overlaps next booking")
        self._bookings.insert(index, booking)
        return booking

    def cancel(self, name: str):
        for index, booking in enumerate(self._bookings):
            if booking.name == name:
                return self._bookings.pop(index)
        raise KeyError(name)

    def free_slots(self, start: int, end: int, duration: int):
        if start >= end or duration <= 0:
            raise ValueError("invalid window or duration")
        cursor = start
        for booking in self._bookings:
            if booking.end <= cursor:
                continue
            if booking.start >= end:
                break
            if booking.start - cursor >= duration:
                yield (cursor, min(booking.start, end))
            cursor = max(cursor, booking.end)
        if end - cursor >= duration:
            yield (cursor, end)

if __name__ == "__main__":
    c = Calendar()
    c.add(9, 10, "standup")
    c.add(11, 12, "review")
    print(list(c.free_slots(8, 14, 1)))
