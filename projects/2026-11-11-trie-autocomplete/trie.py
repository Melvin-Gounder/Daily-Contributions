"""Unicode-aware prefix suggestions using a trie."""
class Node:
    def __init__(self):
        self.children={}; self.weight=None

class Autocomplete:
    def __init__(self): self.root=Node()
    def set(self,word,weight):
        if not isinstance(word,str) or not word: raise ValueError("word must be nonempty")
        if type(weight) is not int or weight<0: raise ValueError("weight must be nonnegative integer")
        node=self.root
        for char in word: node=node.children.setdefault(char,Node())
        node.weight=weight
    def delete(self,word):
        node=self.root; parents=[]
        for char in word:
            if char not in node.children: return False
            parents.append((node,char)); node=node.children[char]
        if node.weight is None: return False
        node.weight=None
        for parent,char in reversed(parents):
            child=parent.children[char]
            if child.weight is not None or child.children: break
            del parent.children[char]
        return True
    def suggest(self,prefix="",limit=5):
        if limit<0: raise ValueError("limit must be nonnegative")
        node=self.root
        for char in prefix:
            if char not in node.children: return []
            node=node.children[char]
        results=[]; stack=[(prefix,node)]
        while stack:
            word,current=stack.pop()
            if current.weight is not None: results.append((word,current.weight))
            for char,child in current.children.items(): stack.append((word+char,child))
        return sorted(results,key=lambda x:(-x[1],x[0]))[:limit]
if __name__=="__main__":
    t=Autocomplete()
    for word,score in [("cat",3),("car",5),("cart",2)]: t.set(word,score)
    print(t.suggest("ca"))
