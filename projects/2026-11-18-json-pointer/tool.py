"""Read-only RFC 6901 JSON Pointer navigation."""
import json
def tokens(pointer):
    if not isinstance(pointer,str): raise TypeError("pointer must be string")
    if pointer=="": return []
    if not pointer.startswith("/"): raise ValueError("pointer must begin with /")
    result=[]
    for part in pointer[1:].split("/"):
        i=0;out=""
        while i<len(part):
            if part[i]=="~":
                if i+1>=len(part) or part[i+1] not in "01": raise ValueError("bad pointer escape")
                out+="/" if part[i+1]=="1" else "~"
                i+=2
            else: out+=part[i];i+=1
        result.append(out)
    return result
def resolve(document,pointer):
    current=document
    for part in tokens(pointer):
        if isinstance(current,dict):
            if part not in current: raise KeyError(part)
            current=current[part]
        elif isinstance(current,list):
            if not part.isascii() or not part.isdecimal() or (len(part)>1 and part[0]=="0"):
                raise IndexError("invalid array index")
            index=int(part)
            current=current[index]
        else: raise TypeError("cannot descend into scalar")
    return current
if __name__=="__main__":
    obj={"a/b":[{"~key":7}]}
    print(resolve(obj,"/a~1b/0/~0key"))
