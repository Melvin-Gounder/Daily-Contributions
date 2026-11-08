import json, os, tempfile
from pathlib import Path
class ConflictError(RuntimeError): pass
class Store:
    def __init__(self,path): self.path=Path(path)
    def read(self):
        if not self.path.exists(): return {"revision":0,"data":{}}
        with self.path.open(encoding="utf8") as f: value=json.load(f)
        if not isinstance(value,dict) or type(value.get("revision")) is not int or not isinstance(value.get("data"),dict): raise ValueError("invalid document")
        return value
    def write(self,data,expected_revision):
        if not isinstance(data,dict): raise TypeError("data must be dict")
        current=self.read()
        if current["revision"]!=expected_revision: raise ConflictError("stale revision")
        encoded=json.dumps({"revision":expected_revision+1,"data":data},allow_nan=False,indent=2)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        tmp=None
        try:
            with tempfile.NamedTemporaryFile("w",encoding="utf8",dir=self.path.parent,delete=False) as f:
                tmp=f.name; f.write(encoded+"\n"); f.flush(); os.fsync(f.fileno())
            os.replace(tmp,self.path); tmp=None
        finally:
            if tmp is not None: os.unlink(tmp)
        return expected_revision+1
if __name__=="__main__":
    with tempfile.TemporaryDirectory() as d:
        s=Store(Path(d)/"settings.json"); print(s.write({"theme":"dark"},0),s.read())
