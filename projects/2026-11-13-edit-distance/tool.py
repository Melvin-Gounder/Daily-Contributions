"""Levenshtein edit distance with a reproducible minimal edit script."""
def align(source: str, target: str):
    n,m=len(source),len(target)
    dp=[[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1): dp[i][0]=i
    for j in range(m+1): dp[0][j]=j
    for i in range(1,n+1):
        for j in range(1,m+1):
            dp[i][j]=min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+(source[i-1]!=target[j-1]))
    i,j=n,m; steps=[]
    while i or j:
        if i and j and source[i-1]==target[j-1] and dp[i][j]==dp[i-1][j-1]:
            steps.append(("keep",source[i-1]));i-=1;j-=1
        elif i and j and dp[i][j]==dp[i-1][j-1]+1:
            steps.append(("replace",target[j-1]));i-=1;j-=1
        elif i and dp[i][j]==dp[i-1][j]+1:
            steps.append(("delete",source[i-1]));i-=1
        else:
            steps.append(("insert",target[j-1]));j-=1
    return dp[n][m],list(reversed(steps))

def replay(source,steps):
    pos=0;out=[]
    for op,char in steps:
        if op=="keep":
            if pos>=len(source) or source[pos]!=char: raise ValueError("invalid keep")
            out.append(char);pos+=1
        elif op=="delete":
            if pos>=len(source) or source[pos]!=char: raise ValueError("invalid delete")
            pos+=1
        elif op=="replace":
            if pos>=len(source): raise ValueError("invalid replace")
            pos+=1;out.append(char)
        elif op=="insert": out.append(char)
        else: raise ValueError("unknown operation")
    if pos!=len(source): raise ValueError("unconsumed source")
    return "".join(out)

if __name__=="__main__":
    distance,steps=align("kitten","sitting")
    print(distance,steps,replay("kitten",steps))
