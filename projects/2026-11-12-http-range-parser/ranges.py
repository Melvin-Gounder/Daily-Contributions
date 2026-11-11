import re
from dataclasses import dataclass

class RangeNotSatisfiable(ValueError):
    pass

@dataclass(frozen=True)
class ByteRange:
    start: int
    end: int
    total: int

    @property
    def length(self):
        return self.end-self.start+1

    @property
    def content_range(self):
        return f"bytes {self.start}-{self.end}/{self.total}"

def parse_range(header, size):
    """Parse a single HTTP bytes range; reject multipart requests explicitly."""
    if not isinstance(size,int) or isinstance(size,bool) or size < 0:
        raise ValueError("invalid resource size")
    if not isinstance(header,str):
        raise ValueError("header must be a string")
    match=re.fullmatch(r"bytes=(\d*)-(\d*)",header.strip(),flags=re.IGNORECASE)
    if not match:
        raise ValueError("unsupported or malformed Range header")
    first,last=match.groups()
    if not first and not last:
        raise ValueError("empty range")
    if size == 0:
        raise RangeNotSatisfiable("empty resource")
    if first:
        start=int(first)
        end=int(last) if last else size-1
        if last and end < start:
            raise RangeNotSatisfiable("reversed range")
        if start >= size:
            raise RangeNotSatisfiable("range starts beyond resource")
        return ByteRange(start,min(end,size-1),size)
    suffix=int(last)
    if suffix == 0:
        raise RangeNotSatisfiable("zero-length suffix")
    return ByteRange(max(0,size-suffix),size-1,size)

if __name__ == "__main__":
    print(parse_range("bytes=-20",100).content_range)
