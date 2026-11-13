import math
import time

class TokenBucket:
    def __init__(self,capacity,refill_per_second,clock=time.monotonic):
        if not all(isinstance(x,(int,float)) and math.isfinite(x) and x>0 for x in (capacity,refill_per_second)):
            raise ValueError("capacity and rate must be positive finite numbers")
        self.capacity=float(capacity)
        self.rate=float(refill_per_second)
        self.clock=clock
        self.last=float(clock())
        self.tokens=self.capacity

    def acquire(self,cost=1):
        if not isinstance(cost,(int,float)) or not math.isfinite(cost) or cost<=0 or cost>self.capacity:
            raise ValueError("invalid cost")
        now=float(self.clock())
        if now<self.last: raise ValueError("clock moved backwards")
        self.tokens=min(self.capacity,self.tokens+(now-self.last)*self.rate)
        self.last=now
        if self.tokens+1e-12>=cost:
            self.tokens=max(0.0,self.tokens-cost)
            return True,0.0
        return False,(cost-self.tokens)/self.rate

if __name__=="__main__":
    bucket=TokenBucket(3,1)
    print([bucket.acquire()[0] for _ in range(5)])
