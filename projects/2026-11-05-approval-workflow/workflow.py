"""State-machine approval workflow: python workflow.py [test]."""
from dataclasses import dataclass
import unittest,sys

@dataclass(frozen=True)
class Rule:
    source:str
    event:str
    target:str
    guard:str=""

class Machine:
    def __init__(self, initial, rules):
        self.state=initial
        self.rules={}
        self.history=[]
        for rule in rules:
            key=(rule.source,rule.event)
            if key in self.rules: raise ValueError("duplicate transition")
            self.rules[key]=rule
    def trigger(self,event,context=None):
        context=context or {}
        rule=self.rules.get((self.state,event))
        if rule is None: raise ValueError("invalid transition")
        if rule.guard and not context.get(rule.guard):
            raise PermissionError("guard not satisfied: "+rule.guard)
        old=self.state
        self.state=rule.target
        self.history.append((old,event,self.state))
        return self.state

def example():
    return Machine("draft",[
        Rule("draft","submit","review"),
        Rule("review","approve","approved","reviewer"),
        Rule("review","reject","draft"),
        Rule("approved","publish","published","ready"),
        Rule("published","archive","archived")])

class Tests(unittest.TestCase):
    def test_happy(self):
        m=example()
        m.trigger("submit")
        m.trigger("approve",{"reviewer":"QA"})
        self.assertEqual(m.trigger("publish",{"ready":True}),"published")
        self.assertEqual(len(m.history),3)
    def test_guard(self):
        m=example()
        m.trigger("submit")
        with self.assertRaises(PermissionError): m.trigger("approve")
        self.assertEqual(m.state,"review")
    def test_reject(self):
        m=example()
        m.trigger("submit")
        self.assertEqual(m.trigger("reject"),"draft")
    def test_invalid(self):
        with self.assertRaises(ValueError): example().trigger("publish")
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            Machine("a",[Rule("a","go","b"),Rule("a","go","c")])

if __name__=="__main__":
    if sys.argv[1:]==["test"]: unittest.main(argv=[sys.argv[0]])
    else:
        m=example()
        for event,ctx in [("submit",{}),("approve",{"reviewer":"QA"}),("publish",{"ready":True})]:
            print(event,"=>",m.trigger(event,ctx))
        print("History:",m.history)
