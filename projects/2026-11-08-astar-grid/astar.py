import heapq
def path(grid,start,goal):
    if not grid or not grid[0] or any(len(r)!=len(grid[0]) for r in grid): raise ValueError("rectangular grid required")
    h,w=len(grid),len(grid[0])
    if any(v not in (0,1) for row in grid for v in row): raise ValueError("cells must be 0 or 1")
    for p in (start,goal):
        if len(p)!=2 or not (0<=p[0]<h and 0<=p[1]<w) or grid[p[0]][p[1]]: raise ValueError("invalid endpoint")
    heuristic=lambda p:abs(p[0]-goal[0])+abs(p[1]-goal[1])
    heap=[(heuristic(start),0,start)]; best={start:0}; prev={}
    while heap:
        _,cost,node=heapq.heappop(heap)
        if cost!=best[node]: continue
        if node==goal:
            result=[node]
            while result[-1]!=start: result.append(prev[result[-1]])
            return list(reversed(result)),cost
        r,c=node
        for p in ((r-1,c),(r,c-1),(r,c+1),(r+1,c)):
            y,x=p
            if 0<=y<h and 0<=x<w and not grid[y][x] and cost+1<best.get(p,float("inf")):
                best[p]=cost+1;prev[p]=node
                heapq.heappush(heap,(cost+1+heuristic(p),cost+1,p))
    return [],None
if __name__=="__main__": print(path([[0,0,0],[0,1,0],[0,0,0]],(0,0),(2,2)))
