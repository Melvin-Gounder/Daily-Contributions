"""Optimal matrix-chain parenthesization using dynamic programming."""
def optimize(dimensions):
    if not isinstance(dimensions,(list,tuple)) or len(dimensions)<2:
        raise ValueError("at least one matrix required")
    if any(not isinstance(d,int) or isinstance(d,bool) or d<=0 for d in dimensions):
        raise ValueError("dimensions must be positive integers")
    n=len(dimensions)-1
    cost=[[0]*n for _ in range(n)]
    split=[[None]*n for _ in range(n)]
    for length in range(2,n+1):
        for i in range(n-length+1):
            j=i+length-1
            candidates=[(cost[i][k]+cost[k+1][j]+dimensions[i]*dimensions[k+1]*dimensions[j+1],k)
                        for k in range(i,j)]
            cost[i][j],split[i][j]=min(candidates)
    def render(i,j):
        if i==j: return f"A{i+1}"
        k=split[i][j]
        return f"({render(i,k)} × {render(k+1,j)})"
    return cost[0][n-1],render(0,n-1)
if __name__=="__main__":
    print(optimize([30,35,15,5,10,20,25]))
