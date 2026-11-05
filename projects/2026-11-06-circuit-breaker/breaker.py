"""Synchronous circuit breaker with injectable monotonic clock."""
import time
from enum import Enum
class State(Enum):
 CLOSED="closed"; OPEN="open"; HALF_OPEN="half-open"
class CircuitOpen(RuntimeError): pass
class Breaker:
 def __init__(self,threshold=3,cooldown=30,clock=time.monotonic):
  if type(threshold)!=int or threshold<1 or cooldown<=0: raise ValueError("invalid settings")
  self.threshold=threshold; self.cooldown=cooldown; self.clock=clock
  self.state=State.CLOSED; self.failures=0; self.opened=None; self.probing=False
 def trip(self):
  self.state=State.OPEN; self.opened=self.clock()
 def call(self,fn,*args,**kwargs):
  if self.state==State.OPEN:
   if self.clock()-self.opened<self.cooldown: raise CircuitOpen("dependency unavailable")
   self.state=State.HALF_OPEN
  if self.state==State.HALF_OPEN:
   if self.probing: raise CircuitOpen("probe in progress")
   self.probing=True
  try: result=fn(*args,**kwargs)
  except Exception:
   if self.state==State.HALF_OPEN: self.trip()
   else:
    self.failures+=1
    if self.failures>=self.threshold: self.trip()
   raise
  else:
   self.state=State.CLOSED; self.failures=0; self.opened=None
   return result
  finally: self.probing=False
if __name__=="__main__":
 b=Breaker(2)
 def fail(): raise ConnectionError("offline")
 for i in range(3):
  try: b.call(fail)
  except (ConnectionError,CircuitOpen) as e: print(type(e).__name__,b.state.value)
