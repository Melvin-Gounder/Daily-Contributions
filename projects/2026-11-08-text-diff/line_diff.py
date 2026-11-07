import argparse
from pathlib import Path
def diff(before,after):
    a,b=list(before),list(after);n,m=len(a),len(b)
    dp=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            dp[i][j]=1+dp[i+1][j+1] if a[i]==b[j] else max(dp[i+1][j],dp[i][j+1])
    i=j=0;out=[]
    while i<n or j<m:
        if i<n and j<m and a[i]==b[j]:out.append((" ",a[i]));i+=1;j+=1
        elif i<n and (j==m or dp[i+1][j]>=dp[i][j+1]):out.append(("-",a[i]));i+=1
        else:out.append(("+",b[j]));j+=1
    return out
def apply(before,edits):
    source=iter(before);out=[];sentinel=object()
    for op,line in edits:
        if op in (" ","-") and next(source,sentinel)!=line:raise ValueError("source mismatch")
        if op in (" ","+"):out.append(line)
        if op not in (" ","-","+"):raise ValueError("invalid operation")
    if next(source,sentinel) is not sentinel:raise ValueError("unconsumed source")
    return out
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("before");p.add_argument("after");a=p.parse_args()
    for op,line in diff(Path(a.before).read_text().splitlines(),Path(a.after).read_text().splitlines()):print(op+line)
