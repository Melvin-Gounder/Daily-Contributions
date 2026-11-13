from pathlib import Path
import os

class RotatingLog:
    def __init__(self,path,max_bytes=1024,backups=3):
        if not isinstance(max_bytes,int) or max_bytes<=0 or not isinstance(backups,int) or backups<0:
            raise ValueError("invalid retention settings")
        self.path=Path(path)
        self.max_bytes=max_bytes
        self.backups=backups
        self.path.parent.mkdir(parents=True,exist_ok=True)

    def write(self,line):
        if not isinstance(line,str): raise TypeError("line must be text")
        data=(line.rstrip("\n")+"\n").encode("utf-8")
        if len(data)>self.max_bytes: raise ValueError("single line exceeds max_bytes")
        size=self.path.stat().st_size if self.path.exists() else 0
        if size+len(data)>self.max_bytes:
            self._rotate()
        with self.path.open("ab") as f: f.write(data)

    def _rotate(self):
        if self.backups==0:
            self.path.write_bytes(b"")
            return
        oldest=Path(str(self.path)+"."+str(self.backups))
        oldest.unlink(missing_ok=True)
        for i in range(self.backups-1,0,-1):
            src=Path(str(self.path)+"."+str(i))
            if src.exists(): os.replace(src,str(self.path)+"."+str(i+1))
        if self.path.exists(): os.replace(self.path,str(self.path)+".1")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("path"); p.add_argument("message"); p.add_argument("--max-bytes",type=int,default=1024)
    args=p.parse_args(); RotatingLog(args.path,args.max_bytes).write(args.message)
