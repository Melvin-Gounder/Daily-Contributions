"""Deficit round-robin scheduler for variable-cost jobs."""
from collections import deque
class Scheduler:
 def __init__(self,quantum):
  if not quantum or any(type(q)!=int or q<=0 for q in quantum.values()): raise ValueError("positive quanta required")
  self.quantum=dict(quantum); self.queues={k:deque() for k in quantum}
  self.credit={k:0 for k in quantum}; self.names=list(quantum); self.position=0
 def enqueue(self,name,item,cost):
  if name not in self.queues: raise KeyError(name)
  if type(cost)!=int or cost<=0: raise ValueError("positive cost required")
  self.queues[name].append((item,cost))
 def drain(self):
  while any(self.queues.values()):
   name=self.names[self.position]; self.position=(self.position+1)%len(self.names)
   queue=self.queues[name]
   if not queue:
    self.credit[name]=0; continue
   self.credit[name]+=self.quantum[name]
   while queue and queue[0][1]<=self.credit[name]:
    item,cost=queue.popleft(); self.credit[name]-=cost
    yield name,item
   if not queue: self.credit[name]=0
if __name__=="__main__":
 s=Scheduler({"video":3,"email":1})
 for i in range(4):
  s.enqueue("video",f"frame-{i}",2); s.enqueue("email",f"mail-{i}",1)
 print(list(s.drain()))
