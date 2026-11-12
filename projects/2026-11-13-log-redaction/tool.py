"""Copy and redact nested JSON-compatible events without mutating input."""
from collections.abc import Mapping
SENSITIVE={"password","secret","token","api_key","authorization","access_token","refresh_token"}
def redact(value,extra_keys=()):
    keys=SENSITIVE|{str(k).casefold() for k in extra_keys}
    def visit(obj,active):
        if isinstance(obj,(dict,list,tuple)):
            ident=id(obj)
            if ident in active: raise ValueError("cyclic event")
            active.add(ident)
            try:
                if isinstance(obj,dict):
                    if not all(isinstance(k,str) for k in obj): raise TypeError("event keys must be strings")
                    return {k:("[REDACTED]" if k.casefold() in keys else visit(v,active)) for k,v in obj.items()}
                return [visit(v,active) for v in obj]
            finally: active.remove(ident)
        if obj is None or isinstance(obj,(str,int,float,bool)): return obj
        raise TypeError("unsupported event value")
    return visit(value,set())
if __name__=="__main__":
    print(redact({"user":"sam","auth":{"token":"private","ok":True}}))
