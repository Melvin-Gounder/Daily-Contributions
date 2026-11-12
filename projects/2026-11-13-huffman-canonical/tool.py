"""Canonical Huffman code construction."""
import heapq,itertools
def codebook(frequencies):
    if not frequencies or any(type(k) is not str or len(k)!=1 or type(v) is not int or v<=0 for k,v in frequencies.items()):
        raise ValueError("single-character symbols and positive integer frequencies required")
    counter=itertools.count()
    heap=[(v,next(counter),k) for k,v in sorted(frequencies.items())]
    heapq.heapify(heap)
    if len(heap)==1: return {heap[0][2]:"0"}
    while len(heap)>1:
        a=heapq.heappop(heap);b=heapq.heappop(heap)
        heapq.heappush(heap,(a[0]+b[0],next(counter),(a[2],b[2])))
    lengths={}
    def walk(node,depth):
        if isinstance(node,str): lengths[node]=depth
        else: walk(node[0],depth+1);walk(node[1],depth+1)
    walk(heap[0][2],0)
    result={};code=0;previous=0
    for symbol,length in sorted(lengths.items(),key=lambda item:(item[1],item[0])):
        code<<=length-previous
        result[symbol]=format(code,"0%db"%length)
        code+=1;previous=length
    return result
def encode(text,codes): return "".join(codes[c] for c in text)
def decode(bits,codes):
    reverse={v:k for k,v in codes.items()};out=[];prefix=""
    for bit in bits:
        if bit not in "01": raise ValueError("nonbinary input")
        prefix+=bit
        if prefix in reverse: out.append(reverse[prefix]);prefix=""
    if prefix: raise ValueError("truncated code")
    return "".join(out)
if __name__=="__main__":
    c=codebook({"A":5,"B":2,"C":1});print(c,encode("ABCA",c))
