"""Stream Base64 without loading entire files."""
import argparse
import base64
def encode(source,target,chunk_size=65535):
    if chunk_size<=0: raise ValueError("chunk_size")
    carry=b""
    while True:
        block=source.read(chunk_size)
        if not block: break
        data=carry+block
        end=len(data)//3*3
        target.write(base64.b64encode(data[:end]))
        carry=data[end:]
    if carry: target.write(base64.b64encode(carry))
def decode(source,target,chunk_size=65536):
    if chunk_size<=0: raise ValueError("chunk_size")
    carry=b""
    while True:
        block=source.read(chunk_size)
        if not block: break
        data=carry+block
        end=len(data)//4*4
        if end:
            target.write(base64.b64decode(data[:end],validate=True))
        carry=data[end:]
    if carry: raise ValueError("truncated Base64")
def main():
    p=argparse.ArgumentParser(description="Strict streaming Base64 converter")
    p.add_argument("mode",choices=["encode","decode"])
    p.add_argument("source")
    p.add_argument("destination")
    args=p.parse_args()
    with open(args.source,"rb") as source,open(args.destination,"wb") as dest:
        (encode if args.mode=="encode" else decode)(source,dest)
if __name__=="__main__": main()
