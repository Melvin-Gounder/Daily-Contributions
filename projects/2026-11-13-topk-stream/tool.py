"""Maintain k best records without retaining the full input."""
import heapq,math
def top_k(records,k):
    if type(k) is not int or k<0: raise ValueError("k must be nonnegative integer")
    heap=[]
    for index,(name,score) in enumerate(records):
        if not isinstance(name,str) or not name: raise ValueError("invalid name")
        if isinstance(score,bool) or not isinstance(score,(int,float)) or not math.isfinite(score):
            raise ValueError("invalid score")
        if k==0: continue
        entry=(score,-index,name)
        if len(heap)<k: heapq.heappush(heap,entry)
        elif entry>heap[0]: heapq.heapreplace(heap,entry)
    return [(name,score) for score,neg_index,name in sorted(heap,reverse=True)]
if __name__=="__main__":
    print(top_k([("A",7),("B",9),("C",9)],2))
