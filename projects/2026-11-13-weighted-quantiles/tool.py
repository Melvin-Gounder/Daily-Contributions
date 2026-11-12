"""Discrete weighted quantiles using exact Fraction arithmetic."""
from fractions import Fraction
def quantile(observations, probability):
    p=Fraction(probability)
    if not 0<=p<=1: raise ValueError("probability outside [0,1]")
    merged={}
    for value,weight in observations:
        if isinstance(value,bool) or isinstance(weight,bool): raise ValueError("boolean not supported")
        v,w=Fraction(value),Fraction(weight)
        if w<=0: raise ValueError("weights must be positive")
        merged[v]=merged.get(v,Fraction(0))+w
    if not merged: raise ValueError("empty observations")
    total=sum(merged.values());running=Fraction(0)
    for value,weight in sorted(merged.items()):
        running+=weight
        if running/total>=p: return value
    raise AssertionError("unreachable")
def median(observations): return quantile(observations,Fraction(1,2))
if __name__=="__main__":
    print(median([(1,1),(10,3),(100,1)]))
