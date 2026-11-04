"""Inventory reorder planner: python stock.py [test]."""
from dataclasses import dataclass
from decimal import Decimal,ROUND_CEILING
import unittest,sys

@dataclass(frozen=True)
class Item:
    sku:str
    on_hand:int
    reserved:int
    demand:Decimal
    lead_days:int
    safety_days:int
    pack:int=1
    def __post_init__(self):
        if not self.sku or min(self.on_hand,self.reserved,self.lead_days,self.safety_days)<0:
            raise ValueError("invalid fields")
        if self.reserved>self.on_hand or self.pack<1:
            raise ValueError("invalid stock")
        if not self.demand.is_finite() or self.demand<0:
            raise ValueError("invalid demand")

def recommend(item):
    available=item.on_hand-item.reserved
    threshold=int((item.demand*(item.lead_days+item.safety_days))
                  .to_integral_value(rounding=ROUND_CEILING))
    shortage=max(0,threshold-available)
    order=((shortage+item.pack-1)//item.pack)*item.pack
    return {"sku":item.sku,"available":available,"reorder_point":threshold,"order":order}

def plan(items):
    seen=set()
    result=[]
    for item in items:
        if item.sku in seen: raise ValueError("duplicate SKU")
        seen.add(item.sku)
        result.append(recommend(item))
    return sorted(result,key=lambda x:(-x["order"],x["sku"]))

class Tests(unittest.TestCase):
    def test_pack(self):
        a=Item("A",10,2,Decimal("2.5"),4,1,6)
        self.assertEqual(recommend(a)["order"],6)
    def test_threshold(self):
        a=Item("A",0,0,Decimal("0.1"),1,0)
        self.assertEqual(recommend(a)["reorder_point"],1)
    def test_no_order(self):
        a=Item("A",100,0,Decimal("1"),2,1)
        self.assertEqual(recommend(a)["order"],0)
    def test_duplicate(self):
        a=Item("A",0,0,Decimal("1"),1,0)
        with self.assertRaises(ValueError): plan([a,a])
    def test_reserved(self):
        a=Item("A",10,8,Decimal("2"),2,0)
        self.assertEqual(recommend(a)["order"],2)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            Item("A",1,2,Decimal("1"),1,0)

if __name__=="__main__":
    if sys.argv[1:]==["test"]: unittest.main(argv=[sys.argv[0]])
    else:
        for row in plan([Item("PENS",12,4,Decimal("3.2"),3,2,10),
                         Item("PAPER",20,5,Decimal("6"),4,1,5)]):
            print(row)
