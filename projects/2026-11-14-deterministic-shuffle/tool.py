import hashlib

class HashStream:
    """Deterministic byte stream for reproducible experiments, not cryptography."""
    def __init__(self,seed):
        if not isinstance(seed,(str,bytes)): raise TypeError("seed must be text or bytes")
        self.seed=seed.encode("utf-8") if isinstance(seed,str) else seed
        self.counter=0
    def next_bytes(self):
        data=hashlib.sha256(self.seed+self.counter.to_bytes(8,"big")).digest()
        self.counter+=1
        return data
    def randbelow(self,n):
        if not isinstance(n,int) or n<=0 or n>2**256: raise ValueError("invalid range")
        limit=2**256-(2**256 % n)
        while True:
            number=int.from_bytes(self.next_bytes(),"big")
            if number<limit: return number%n

def shuffle(items,seed):
    result=list(items)
    stream=HashStream(seed)
    for i in range(len(result)-1,0,-1):
        j=stream.randbelow(i+1)
        result[i],result[j]=result[j],result[i]
    return result

if __name__=="__main__":
    print(shuffle(list(range(10)),"demo"))
