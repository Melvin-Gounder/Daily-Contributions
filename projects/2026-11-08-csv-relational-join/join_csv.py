import csv,argparse
from collections import defaultdict
def join(left,right,output,left_key,right_key,how="inner"):
    if how not in ("inner","left"): raise ValueError("join mode")
    with open(right,newline="",encoding="utf8") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or right_key not in reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames): raise ValueError("right header")
        fields=reader.fieldnames;index=defaultdict(list)
        for row in reader:
            if None in row or None in row.values(): raise ValueError("right row")
            index[row[right_key]].append(row)
    with open(left,newline="",encoding="utf8") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or left_key not in reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames): raise ValueError("left header")
        used=set(reader.fieldnames);rename={}
        for field in fields:
            if field==right_key: continue
            name=field
            while name in used: name="right_"+name
            rename[field]=name;used.add(name)
        with open(output,"w",newline="",encoding="utf8") as dest:
            writer=csv.DictWriter(dest,fieldnames=list(reader.fieldnames)+list(rename.values()));writer.writeheader()
            for row in reader:
                if None in row or None in row.values(): raise ValueError("left row")
                matches=index.get(row[left_key],[])
                if not matches and how=="left": writer.writerow({**row,**{v:"" for v in rename.values()}})
                for match in matches: writer.writerow({**row,**{v:match[k] for k,v in rename.items()}})
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("left");p.add_argument("right");p.add_argument("output")
    p.add_argument("--left-key",required=True);p.add_argument("--right-key",required=True);p.add_argument("--how",choices=["inner","left"],default="inner")
    a=p.parse_args();join(a.left,a.right,a.output,a.left_key,a.right_key,a.how)
