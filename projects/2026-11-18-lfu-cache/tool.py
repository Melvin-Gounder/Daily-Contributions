from collections import defaultdict,OrderedDict
class LFUCache:
    def __init__(self,capacity):
        if not isinstance(capacity,int) or capacity<0: raise ValueError("capacity")
        self.capacity=capacity
        self.values={}
        self.counts={}
        self.buckets=defaultdict(OrderedDict)
        self.minimum=0
    def _touch(self,key):
        n=self.counts[key]
        del self.buckets[n][key]
        if not self.buckets[n]:
            del self.buckets[n]
            if self.minimum==n: self.minimum=n+1
        self.counts[key]=n+1
        self.buckets[n+1][key]=None
    def get(self,key,default=None):
        if key not in self.values: return default
        self._touch(key)
        return self.values[key]
    def put(self,key,value):
        if not self.capacity: return
        if key in self.values:
            self.values[key]=value
            self._touch(key)
            return
        if len(self.values)==self.capacity:
            victim,_=self.buckets[self.minimum].popitem(last=False)
            if not self.buckets[self.minimum]: del self.buckets[self.minimum]
            del self.values[victim]
            del self.counts[victim]
        self.values[key]=value
        self.counts[key]=1
        self.buckets[1][key]=None
        self.minimum=1
if __name__=="__main__":
    c=LFUCache(2)
    c.put("a",1);c.put("b",2);c.get("a");c.put("c",3)
    print(c.values)
