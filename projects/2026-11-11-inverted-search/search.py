"""Small in-memory BM25 document search index."""
from collections import Counter
import math
import re

def tokenize(text):
    return re.findall(r"[a-z0-9]+",text.lower())

class SearchIndex:
    def __init__(self,k1=1.2,b=0.75):
        if k1<=0 or not 0<=b<=1: raise ValueError("invalid BM25 parameters")
        self.k1=k1; self.b=b; self.docs={}
    def add(self,identifier,text):
        if not isinstance(text,str): raise TypeError("text must be string")
        self.docs[identifier]=Counter(tokenize(text))
    def remove(self,identifier):
        self.docs.pop(identifier,None)
    def search(self,query,limit=10):
        if limit<0: raise ValueError("limit must be nonnegative")
        n=len(self.docs)
        if not n: return []
        terms=set(tokenize(query))
        if not terms: return []
        avg=sum(sum(d.values()) for d in self.docs.values())/n
        matches=[]
        for identifier,counts in self.docs.items():
            length=sum(counts.values()); score=0.0; explanation={}
            for term in terms:
                tf=counts[term]
                if not tf: continue
                df=sum(term in doc for doc in self.docs.values())
                idf=math.log(1+(n-df+0.5)/(df+0.5))
                value=idf*tf*(self.k1+1)/(tf+self.k1*(1-self.b+self.b*length/avg))
                score+=value; explanation[term]=round(value,6)
            if score>0: matches.append((identifier,score,explanation))
        return sorted(matches,key=lambda row:(-row[1],str(row[0])))[:limit]
if __name__=="__main__":
    index=SearchIndex()
    index.add("a","network security network")
    index.add("b","database security")
    print(index.search("network security"))
