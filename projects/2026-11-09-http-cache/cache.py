from dataclasses import dataclass
@dataclass(frozen=True)
class Decision:
    storable: bool
    fresh: bool
    reason: str
def parse(header):
    result={}
    for item in header.split(","):
        item=item.strip()
        if item:
            key,sep,value=item.partition("=")
            result[key.strip().lower()]=value.strip().strip('"') if sep else True
    return result
def evaluate(header,age,shared=True,authenticated=False):
    if age<0: raise ValueError("negative age")
    cc=parse(header)
    if "no-store" in cc: return Decision(False,False,"no-store")
    if shared and "private" in cc: return Decision(False,False,"private")
    if shared and authenticated and not any(k in cc for k in ("public","s-maxage","must-revalidate")):
        return Decision(False,False,"authorization")
    key="s-maxage" if shared and "s-maxage" in cc else "max-age"
    if key not in cc: return Decision(False,False,"no explicit lifetime")
    try: lifetime=int(cc[key])
    except (TypeError,ValueError): raise ValueError("invalid lifetime") from None
    if lifetime<0: raise ValueError("negative lifetime")
    fresh=age<lifetime and "no-cache" not in cc
    return Decision(True,fresh,"fresh" if fresh else "revalidate")
if __name__=="__main__":
    for age in (0,30,60): print(age,evaluate("public, max-age=60",age))
