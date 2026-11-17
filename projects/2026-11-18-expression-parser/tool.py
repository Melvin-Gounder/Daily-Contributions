"""Arithmetic evaluator without eval or dynamic execution."""
import re
TOKENS=re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([()+*/-]))")
def tokenize(source):
    pos=0
    result=[]
    while pos<len(source):
        if source[pos:].strip()=="": break
        match=TOKENS.match(source,pos)
        if not match: raise ValueError(f"invalid character at offset {pos}")
        result.append(match.group(1) or match.group(2))
        pos=match.end()
    return result
class Parser:
    def __init__(self,tokens): self.tokens=tokens;self.pos=0
    def peek(self): return self.tokens[self.pos] if self.pos<len(self.tokens) else None
    def take(self): x=self.peek();self.pos+=1;return x
    def expression(self):
        value=self.term()
        while self.peek() in ("+","-"):
            op=self.take();rhs=self.term()
            value=value+rhs if op=="+" else value-rhs
        return value
    def term(self):
        value=self.factor()
        while self.peek() in ("*","/"):
            op=self.take();rhs=self.factor()
            if op=="/" and rhs==0: raise ZeroDivisionError("division by zero")
            value=value*rhs if op=="*" else value/rhs
        return value
    def factor(self):
        token=self.peek()
        if token is None: raise ValueError("missing operand")
        if token in ("+","-"):
            sign=self.take()
            value=self.factor()
            return value if sign=="+" else -value
        if token=="(":
            self.take();value=self.expression()
            if self.take()!=")": raise ValueError("missing closing parenthesis")
            return value
        if token==")": raise ValueError("unexpected closing parenthesis")
        self.take()
        return float(token)
def evaluate(source):
    parser=Parser(tokenize(source))
    result=parser.expression()
    if parser.peek() is not None: raise ValueError("trailing tokens")
    return result
if __name__=="__main__":
    print(evaluate("2*(3+4)-5/2"))
