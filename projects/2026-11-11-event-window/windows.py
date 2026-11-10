"""Event-time windows with explicit watermark advancement."""
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Window:
    start:int
    end:int
    count:int
    total:float

class Aggregator:
    def __init__(self,width):
        if type(width) is not int or width<=0: raise ValueError("width must be positive integer")
        self.width=width; self.watermark=float("-inf"); self.pending=defaultdict(list)
    def add(self,timestamp,value):
        if type(timestamp) is not int: raise TypeError("timestamp must be integer")
        if not isinstance(value,(int,float)) or isinstance(value,bool):
            raise TypeError("value must be numeric")
        import math
        if not math.isfinite(value): raise ValueError("value must be finite")
        if timestamp<self.watermark: return False
        start=timestamp//self.width*self.width
        if start+self.width<=self.watermark: return False
        self.pending[start].append(value)
        return True
    def advance(self,watermark):
        if watermark<self.watermark: raise ValueError("watermark cannot go backward")
        self.watermark=watermark
        ready=sorted(start for start in self.pending if start+self.width<=watermark)
        result=[]
        for start in ready:
            values=self.pending.pop(start)
            result.append(Window(start,start+self.width,len(values),sum(values)))
        return result
if __name__=="__main__":
    a=Aggregator(10); a.add(9,2); a.add(1,3); print(a.advance(10))
