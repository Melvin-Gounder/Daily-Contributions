import csv,tempfile,unittest
from pathlib import Path
from join_csv import join
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
 def write(self,name,rows):
  p=self.root/name
  with p.open("w",newline="") as f: csv.writer(f).writerows(rows)
  return str(p)
 def read(self,p):
  with open(p,newline="") as f:return list(csv.DictReader(f))
 def test_left_duplicates(self):
  a=self.write("a.csv",[["id","name"],["1","Ana"],["2","Ben"]])
  b=self.write("b.csv",[["key","name"],["1","red"],["1","blue"]]);out=str(self.root/"o.csv")
  join(a,b,out,"id","key","left");rows=self.read(out)
  self.assertEqual(len(rows),3);self.assertEqual([r["right_name"] for r in rows],["red","blue",""])
 def test_inner(self):
  a=self.write("a.csv",[["id"],["1"],["2"]]);b=self.write("b.csv",[["id","v"],["1","ok"]]);out=str(self.root/"o.csv")
  join(a,b,out,"id","id");self.assertEqual(self.read(out),[{"id":"1","v":"ok"}])
if __name__=="__main__":unittest.main()
