"""Deterministic SHA-256 consistent hashing with virtual nodes."""
import bisect, hashlib
def hash_of(s): return int.from_bytes(hashlib.sha256(s.encode()).digest(),"big")
class Ring:
 def __init__(self,replicas=64):
  if type(replicas)!=int or replicas<1: raise ValueError("replicas")
  self.replicas=replicas; self.points=[]; self.nodes=[]; self.members=set()
 def add(self,name):
  if not isinstance(name,str) or not name or name in self.members: raise ValueError("unique nonempty node required")
  self.members.add(name)
  for i in range(self.replicas):
   p=hash_of(f"{len(name)}:{name}:{i}"); j=bisect.bisect_left(self.points,p)
   self.points.insert(j,p); self.nodes.insert(j,name)
 def remove(self,name):
  if name not in self.members: raise KeyError(name)
  self.members.remove(name)
  pairs=[(p,n) for p,n in zip(self.points,self.nodes) if n!=name]
  self.points=[p for p,n in pairs]; self.nodes=[n for p,n in pairs]
 def locate(self,key):
  if not self.points: raise LookupError("empty ring")
  if not isinstance(key,str): raise TypeError("key must be str")
  return self.nodes[bisect.bisect_left(self.points,hash_of(key))%len(self.points)]
if __name__=="__main__":
 r=Ring()
 for n in ("east","west","central"): r.add(n)
 for k in ("user:1","user:2","order:5"): print(k,r.locate(k))
