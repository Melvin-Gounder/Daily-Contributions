from bisect import bisect_right

class IntervalSet:
    """Immutable normalized union of half-open integer intervals."""
    def __init__(self, intervals=()):
        merged = []
        for a,b in sorted(intervals):
            if not isinstance(a,int) or not isinstance(b,int) or a>=b:
                raise ValueError("intervals must have integer start < end")
            if merged and a<=merged[-1][1]:
                merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
            else:
                merged.append((a,b))
        self.ranges=tuple(merged)

    def __contains__(self, value):
        if not isinstance(value,int): return False
        i=bisect_right(self.ranges,(value,float("inf")))-1
        return i>=0 and value<self.ranges[i][1]

    def union(self, other):
        return IntervalSet(self.ranges+other.ranges)

    def intersection(self, other):
        i=j=0
        out=[]
        while i<len(self.ranges) and j<len(other.ranges):
            a,b=self.ranges[i]; c,d=other.ranges[j]
            if max(a,c)<min(b,d): out.append((max(a,c),min(b,d)))
            if b<d: i+=1
            else: j+=1
        return IntervalSet(out)

    def difference(self, other):
        out=[]
        for a,b in self.ranges:
            cursor=a
            for c,d in other.ranges:
                if d<=cursor: continue
                if c>=b: break
                if c>cursor: out.append((cursor,min(c,b)))
                cursor=max(cursor,d)
                if cursor>=b: break
            if cursor<b: out.append((cursor,b))
        return IntervalSet(out)

if __name__=="__main__":
    print(IntervalSet([(1,4),(3,8)]).ranges)
