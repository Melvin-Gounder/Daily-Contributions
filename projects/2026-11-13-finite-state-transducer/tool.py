"""Deterministic stateful text normalization, suitable for chunked input."""
class Normalizer:
    def __init__(self):
        self.pending_space=False;self.started=False
    def feed(self,text):
        out=[]
        for ch in text:
            if ch.isspace():
                if self.started:self.pending_space=True
                continue
            if self.pending_space:
                if ch not in ",.;:!?":out.append(" ")
                self.pending_space=False
            out.append(ch);self.started=True
        return "".join(out)
    def finish(self):
        self.pending_space=False
        return ""
def normalize(text):
    n=Normalizer();return n.feed(text)+n.finish()
if __name__=="__main__":
    print(normalize("  Hello  ,   world!  "))
