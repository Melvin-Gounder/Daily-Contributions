"""Maximum bipartite matching and Konig minimum vertex cover."""
from collections import deque
def solve(edges):
    graph={u:sorted(set(vs),key=str) for u,vs in edges.items()}
    match_right={}
    def augment(u,seen):
        for v in graph[u]:
            if v in seen: continue
            seen.add(v)
            if v not in match_right or augment(match_right[v],seen):
                match_right[v]=u;return True
        return False
    for u in sorted(graph,key=str): augment(u,set())
    match_left={u:v for v,u in match_right.items()}
    # Alternating paths from unmatched left vertices.
    seen_left=set(graph)-set(match_left);seen_right=set()
    queue=deque(sorted(seen_left,key=str))
    while queue:
        u=queue.popleft()
        for v in graph[u]:
            if match_left.get(u)==v or v in seen_right: continue
            seen_right.add(v)
            if v in match_right and match_right[v] not in seen_left:
                w=match_right[v];seen_left.add(w);queue.append(w)
    return match_left,(set(graph)-seen_left,seen_right)
if __name__=="__main__":
    print(solve({"a":[1,2],"b":[2],"c":[1]}))
