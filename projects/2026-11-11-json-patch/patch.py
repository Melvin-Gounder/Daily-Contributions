"""Transactional JSON Patch subset: add/remove/replace/test."""
import copy

class PatchError(ValueError): pass

def parts(pointer):
    if pointer=="": return []
    if not isinstance(pointer,str) or not pointer.startswith("/"):
        raise PatchError("invalid JSON pointer")
    result=[]
    for token in pointer[1:].split("/"):
        import re
        if re.search(r"~(?![01])",token): raise PatchError("invalid escape")
        result.append(token.replace("~1","/").replace("~0","~"))
    return result

def locate(root,tokens):
    value=root
    for token in tokens:
        if isinstance(value,dict):
            if token not in value: raise PatchError("missing key")
            value=value[token]
        elif isinstance(value,list):
            if not token.isdigit() or (len(token)>1 and token[0]=="0"): raise PatchError("invalid index")
            index=int(token)
            if index>=len(value): raise PatchError("index out of range")
            value=value[index]
        else: raise PatchError("cannot traverse scalar")
    return value

def apply(document,operations):
    result=copy.deepcopy(document)
    for op in operations:
        action=op["op"]; tokens=parts(op["path"])
        if action not in {"add","remove","replace","test"}: raise PatchError("unsupported operation")
        if action=="test":
            if locate(result,tokens)!=op["value"]: raise PatchError("test failed")
            continue
        if not tokens:
            if action=="remove": raise PatchError("cannot remove document root")
            result=copy.deepcopy(op["value"]); continue
        parent=locate(result,tokens[:-1]); key=tokens[-1]
        if isinstance(parent,dict):
            if action!="add" and key not in parent: raise PatchError("missing key")
            if action=="remove": del parent[key]
            else: parent[key]=copy.deepcopy(op["value"])
        elif isinstance(parent,list):
            if key=="-" and action=="add": index=len(parent)
            elif key.isdigit() and (len(key)==1 or key[0]!="0"): index=int(key)
            else: raise PatchError("invalid array index")
            if index>len(parent) or (action!="add" and index==len(parent)):
                raise PatchError("array index out of range")
            if action=="add": parent.insert(index,copy.deepcopy(op["value"]))
            elif action=="remove": parent.pop(index)
            else: parent[index]=copy.deepcopy(op["value"])
        else: raise PatchError("cannot modify scalar")
    return result
if __name__=="__main__":
    print(apply({"items":[1,2]},[{"op":"add","path":"/items/-","value":3}]))
