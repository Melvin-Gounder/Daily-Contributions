import hashlib
def digest(data): return hashlib.sha256(data).digest()
def layers(items):
    if not items: raise ValueError("empty tree")
    levels=[[digest(b"\x00"+x) for x in items]]
    while len(levels[-1])>1:
        row=levels[-1]
        levels.append([digest(b"\x01"+row[i]+row[min(i+1,len(row)-1)]) for i in range(0,len(row),2)])
    return levels
def root(items): return layers(items)[-1][0].hex()
def proof(items,index):
    levels=layers(items)
    if not 0<=index<len(levels[0]): raise IndexError(index)
    result=[]
    for row in levels[:-1]:
        result.append((row[min(index^1,len(row)-1)].hex(),bool(index&1)))
        index//=2
    return result
def verify(item,witness,expected):
    h=digest(b"\x00"+item)
    for sibling,left in witness:
        try: other=bytes.fromhex(sibling)
        except ValueError: return False
        if len(other)!=32: return False
        h=digest(b"\x01"+(other+h if left else h+other))
    return h.hex()==expected
if __name__=="__main__":
    items=[b"one",b"two",b"three"]
    print(root(items),verify(items[1],proof(items,1),root(items)))
