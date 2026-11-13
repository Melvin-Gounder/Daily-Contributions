class SmoothWeightedRoundRobin:
    def __init__(self,weights):
        self.weights={}
        self.current={}
        for key,weight in weights.items(): self.set_weight(key,weight)

    def set_weight(self,key,weight):
        if not isinstance(weight,int) or isinstance(weight,bool) or weight<0:
            raise ValueError("weights must be nonnegative integers")
        self.weights[key]=weight
        self.current.setdefault(key,0)
        if weight==0: self.current[key]=0

    def next(self):
        total=sum(self.weights.values())
        if total==0: raise ValueError("no active destinations")
        for key,w in self.weights.items(): self.current[key]+=w
        winner=max((k for k in self.weights if self.weights[k]>0),key=lambda k:self.current[k])
        self.current[winner]-=total
        return winner

if __name__=="__main__":
    scheduler=SmoothWeightedRoundRobin({"a":5,"b":1,"c":1})
    print([scheduler.next() for _ in range(14)])
