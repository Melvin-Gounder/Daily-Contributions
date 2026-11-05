"""Domain-separated SHA-256 Merkle roots and inclusion proofs."""
import hashlib
def leaf(data):
 if not isinstance(data,bytes): raise TypeError("bytes required")
 return hashlib.sha256(b"\x00"+data).digest()
def parent(a,b): return hashlib.sha256(b"\x01"+a+b).digest()
def layers(records):
 if not records: raise ValueError("empty batch")
 result=[[leaf(r) for r in records]]
 while len(result[-1])>1:
  old=result[-1]
  result.append([parent(old[i],old[i+1] if i+1<len(old) else old[i]) for i in range(0,len(old),2)])
 return result
def root(records): return layers(records)[-1][0].hex()
def proof(records,index):
 tree=layers(records)
 if not 0<=index<len(tree[0]): raise IndexError(index)
 witness=[]
 for level in tree[:-1]:
  other=index^1
  if other>=len(level): other=index
  witness.append(("left" if other<index else "right",level[other].hex()))
  index//=2
 return witness
def verify(record,witness,expected):
 try:
  value=leaf(record)
  for side,encoded in witness:
   sibling=bytes.fromhex(encoded)
   if len(sibling)!=32 or side not in ("left","right"): return False
   value=parent(sibling,value) if side=="left" else parent(value,sibling)
  return value.hex()==expected
 except (TypeError,ValueError,AttributeError): return False
if __name__=="__main__":
 batch=[b"alpha",b"beta",b"gamma"]
 print(root(batch),verify(batch[1],proof(batch,1),root(batch)))
