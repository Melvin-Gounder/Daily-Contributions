"""Educational event-sourced ledger: python ledger.py [test]. Not a bank."""
from dataclasses import dataclass
import json,sys,unittest

@dataclass(frozen=True)
class Event:
    event_id:str
    account:str
    kind:str
    cents:int

class Ledger:
    def __init__(self):
        self.events=[]
        self.ids=set()
        self.balances={}
    def apply(self,event):
        if not event.event_id or not event.account or event.kind not in ("credit","debit"):
            raise ValueError("invalid event")
        if type(event.cents) is not int or event.cents<=0:
            raise ValueError("invalid amount")
        if event.event_id in self.ids: raise ValueError("duplicate ID")
        current=self.balances.get(event.account,0)
        change=event.cents if event.kind=="credit" else -event.cents
        if current+change<0: raise ValueError("overdraft")
        self.balances[event.account]=current+change
        self.ids.add(event.event_id)
        self.events.append(event)
    def export(self):
        return "\n".join(json.dumps(vars(e),sort_keys=True) for e in self.events)
    @classmethod
    def replay(cls,data):
        ledger=cls()
        for line in data.splitlines():
            record=json.loads(line)
            if set(record)!={"event_id","account","kind","cents"}:
                raise ValueError("invalid record shape")
            ledger.apply(Event(**record))
        return ledger

class Tests(unittest.TestCase):
    def test_replay(self):
        l=Ledger()
        l.apply(Event("1","A","credit",1000))
        l.apply(Event("2","A","debit",275))
        self.assertEqual(Ledger.replay(l.export()).balances["A"],725)
    def test_overdraft(self):
        l=Ledger()
        with self.assertRaises(ValueError): l.apply(Event("1","A","debit",1))
        self.assertEqual(l.events,[])
    def test_duplicate(self):
        l=Ledger()
        l.apply(Event("1","A","credit",1))
        with self.assertRaises(ValueError): l.apply(Event("1","B","credit",1))
    def test_separate(self):
        l=Ledger()
        l.apply(Event("1","A","credit",1))
        l.apply(Event("2","B","credit",2))
        self.assertEqual(l.balances,{"A":1,"B":2})
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): Ledger().apply(Event("1","A","credit",True))
    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            Ledger.replay('{"event_id":"1","account":"A","kind":"credit"}')

if __name__=="__main__":
    if sys.argv[1:]==["test"]: unittest.main(argv=[sys.argv[0]])
    else:
        l=Ledger()
        l.apply(Event("tx1","savings","credit",5000))
        l.apply(Event("tx2","savings","debit",1250))
        print(l.export())
        print("Balance in cents:",l.balances["savings"])
