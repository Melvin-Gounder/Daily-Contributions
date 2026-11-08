from bisect import bisect_right
def optimize(jobs):
    """jobs: iterable of (start,end,value); returns (value, selected tuples)."""
    jobs = sorted(jobs, key=lambda x: (x[1], x[0]))
    if any(e <= s or v < 0 for s,e,v in jobs):
        raise ValueError("invalid interval or negative value")
    ends = [e for s,e,v in jobs]
    pred = [bisect_right(ends, s, 0, i) for i,(s,e,v) in enumerate(jobs)]
    dp = [0]*(len(jobs)+1)
    for i,(_,_,v) in enumerate(jobs,1):
        dp[i] = max(dp[i-1], v+dp[pred[i-1]])
    chosen=[]
    i=len(jobs)
    while i:
        if jobs[i-1][2]+dp[pred[i-1]] > dp[i-1]:
            chosen.append(jobs[i-1])
            i=pred[i-1]
        else:
            i-=1
    return dp[-1], list(reversed(chosen))
if __name__=="__main__":
    print(optimize([(0,3,5),(2,5,9),(3,6,6),(5,7,4)]))
