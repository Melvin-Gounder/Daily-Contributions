"""Stream CSV records while replacing chosen fields with keyed pseudonyms."""
import argparse
import csv
import hashlib
import hmac
import os

def pseudonym(secret, value):
    if not secret: raise ValueError("nonempty secret required")
    return hmac.new(secret, value.encode("utf-8"), hashlib.sha256).hexdigest()[:32]

def transform(reader, writer, columns, secret):
    fields = reader.fieldnames
    if not fields or len(fields) != len(set(fields)):
        raise ValueError("missing or duplicate CSV headers")
    missing = set(columns) - set(fields)
    if missing: raise ValueError("unknown columns: " + ", ".join(sorted(missing)))
    writer.writeheader()
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("malformed CSV row")
        for column in columns:
            row[column] = pseudonym(secret, row[column])
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--columns", nargs="+", required=True)
    args = parser.parse_args()
    secret = os.environ.get("PSEUDONYM_KEY","").encode()
    if len(secret) < 16: parser.error("set PSEUDONYM_KEY to at least 16 bytes")
    if os.path.abspath(args.source) == os.path.abspath(args.destination):
        parser.error("source and destination must differ")
    with open(args.source,newline="",encoding="utf-8") as src, open(args.destination,"w",newline="",encoding="utf-8") as dst:
        transform(csv.DictReader(src),csv.DictWriter(dst,fieldnames=[] if False else csv.DictReader(open(args.source,newline="",encoding="utf-8")).fieldnames),args.columns,secret)

if __name__ == "__main__": main()
