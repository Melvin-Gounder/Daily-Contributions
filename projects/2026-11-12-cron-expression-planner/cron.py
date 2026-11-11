from datetime import datetime, timedelta

LIMITS = ((0,59),(0,23),(1,31),(1,12),(0,7))

def parse_field(text, low, high):
    result = set()
    for part in text.split(","):
        if not part:
            raise ValueError("empty cron field component")
        base, sep, step_text = part.partition("/")
        step = int(step_text) if sep and step_text.isdecimal() else 1
        if sep and (not step_text.isdecimal() or step < 1):
            raise ValueError("invalid step")
        if base == "*":
            start, end = low, high
        elif "-" in base:
            left, right = base.split("-", 1)
            if not left.isdecimal() or not right.isdecimal():
                raise ValueError("invalid range")
            start, end = int(left), int(right)
        elif base.isdecimal():
            start = int(base)
            end = high if sep else start
        else:
            raise ValueError("invalid cron component")
        if not (low <= start <= end <= high):
            raise ValueError("field outside range")
        result.update(range(start, end+1, step))
    return result

class Cron:
    """Five-field cron with standard OR semantics for restricted day fields."""
    def __init__(self, expression):
        fields = expression.split()
        if len(fields) != 5:
            raise ValueError("expected five fields")
        self.values = [parse_field(s, *bounds) for s,bounds in zip(fields, LIMITS)]
        self.day_wild = fields[2] == "*"
        self.week_wild = fields[4] == "*"

    def matches(self, dt):
        minute, hour, dom, month, dow = self.values
        weekday = (dt.weekday()+1) % 7
        day_match = dt.day in dom
        week_match = weekday in dow or (weekday == 0 and 7 in dow)
        if self.day_wild: date_ok = week_match
        elif self.week_wild: date_ok = day_match
        else: date_ok = day_match or week_match
        return dt.minute in minute and dt.hour in hour and dt.month in month and date_ok

    def next_after(self, dt, max_minutes=527040):
        if max_minutes < 1: raise ValueError("max_minutes must be positive")
        candidate = dt.replace(second=0, microsecond=0) + timedelta(minutes=1)
        for _ in range(max_minutes):
            if self.matches(candidate): return candidate
            candidate += timedelta(minutes=1)
        raise LookupError("no match within search horizon")

if __name__ == "__main__":
    print(Cron("*/15 9-17 * * 1-5").next_after(datetime(2026,11,12,9,0)))
