"""Jump consistent hash maps 64-bit keys to buckets."""
import hashlib
MASK=(1<<64)-1
def bucket(key,count):
    if not isinstance(key,int) or not 0<=key<=MASK: raise ValueError("key must be unsigned 64-bit integer")
    if not isinstance(count,int) or count<=0: raise ValueError("positive bucket count required")
    b,j=-1,0
    while j<count:
        b=j
        key=(key*2862933555777941757+1)&MASK
        j=int((b+1)*(1<<31)/((key>>33)+1))
    return b
def key_hash(text):
    if not isinstance(text,str): raise TypeError("string required")
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8],"big")
def assign(text,count): return bucket(key_hash(text),count)
if __name__=="__main__":
    for key in ("api","database","cache"): print(key,assign(key,7))
